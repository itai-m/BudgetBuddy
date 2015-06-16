from google.appengine.ext.webapp import template
from models.BudgeteerModel import Budgeteer
from models.PasswordTokenRecoveryModel import PasswordTokenRecovery
from api.MailSender import MailSender
import webapp2
import string
import os


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
            if budgeteer:
                self.redirect('/Budgets')
        template_params = dict()
        html = template.render("web/templates/password_recovery.html", template_params)
        self.response.write(html)

    def post(self):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
            if budgeteer:
                self.redirect('/Budgets')

        email = self.request.get("emailAddress")

        template_params = dict()
        if not MailSender.check_if_email_valid(email):
            template_params['emailStatus'] = "Please insert your email address"
            html = template.render("web/templates/password_recovery.html", template_params)
            self.response.write(html)
            return

        budgeteerId = Budgeteer.getBudgeteerIdByEmail(email)

        if budgeteerId:
            budgeteer = Budgeteer.getBudgeteerById(budgeteerId)
            tokenForBudgeteerId = PasswordTokenRecovery.getTokenByBudgeteerId(budgeteerId)
            if tokenForBudgeteerId:
                template_params['emailStatus'] = "An Email with password has already been sent." + \
                                                 " Please wait couple of minutes"
            else:
                PasswordTokenRecovery.addTokenToDataStore(budgeteerId)
                MailSender.send_password_recovery_token(budgeteer.userName,
                                                        budgeteer.email,
                                                        PasswordTokenRecovery.getTokenByBudgeteerId(budgeteerId))
                template_params['emailStatus'] = "An Email with password has already been sent."
        else:
            template_params['emailStatus'] = "There is no such email."

        html = template.render("web/templates/password_recovery.html", template_params)
        self.response.write(html)


class SendNewPasswordHandler(webapp2.RequestHandler):
    def get(self, token):
        budgeteerId = PasswordTokenRecovery.resetPassword(token)
        if budgeteerId:
            budgeteer = Budgeteer.getBudgeteerById(budgeteerId)
            new_pass = ''.join(string.digits[ord(c) % len(string.digits)] for c in os.urandom(16))
            MailSender.send_new_password(budgeteer.userName, budgeteer.email, new_pass)
            budgeteer.password = new_pass
            Budgeteer.updateBudgeteerAccount(budgeteer)
            self.redirect("/Login")
        else:
            self.redirect("/404")

app = webapp2.WSGIApplication([
    ('/PasswordRecovery[\/]?', IndexHandler),
    ('/PasswordRecovery/(.*)', SendNewPasswordHandler)
], debug=True)
