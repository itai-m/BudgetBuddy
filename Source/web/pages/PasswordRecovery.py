from google.appengine.ext.webapp import template
from google.appengine.api import mail
from models.BudgeteerModel import Budgeteer
from models.PasswordTokenRecoveryModel import PasswordTokenRecovery
import webapp2
import string
import os
import time

class MailSender:
    def __init__(self):
        pass

    @staticmethod
    def sendTokenInEmail(toFirstName, toLastName, toAddress, toToken):
        body = """
        Hello,
        Please go to http://budgetbuddy001.appspot.com/PasswordRecovery/{0}
        You will get your new password within a minute after click the link
        """.format(toToken)
        mail.send_mail("BudgetBuddy Support <budgetbuddy00@gmail.com>",
                       toFirstName + " " + toLastName + " <" + toAddress + ">",
                       "Password Recovery", body)

    @staticmethod
    def sendNewPasswordToEmail(toFirstName, toLastName, toAddress, toPass):
        body = """
        Hello,
        Your new password has been set to {0}
        You can login through http://budgetbuddy001.appspot.com/Login
        with your username and new password
        """.format(toPass)
        mail.send_mail("BudgetBuddy Support <budgetbuddy00@gmail.com>",
                       toFirstName + " " + toLastName + " <" + toAddress + ">",
                       "Password Recovery", body)

class IndexHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
            if budgeteer:
                self.redirect('/Budgets')
        template_params = dict()
        html = template.render("web/templates/PasswordRecovery.html", template_params)
        self.response.write(html)

    def post(self):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
            if budgeteer:
                self.redirect('/Budgets')

        email = self.request.get("emailAddress")
        #check email validation

        template_params = dict()
        budgeteerId = Budgeteer.getBudgeteerIdByEmail(email)

        if budgeteerId:
            budgeteer = Budgeteer.getBudgeteerById(budgeteerId)
            tokenForBudgeteerId = PasswordTokenRecovery.getTokenByBudgeteerId(budgeteerId)
            if tokenForBudgeteerId:
                template_params['emailStatus'] = "An Email with password has already been sent." + \
                                                 " Please wait couple of minutes"
            else:
                PasswordTokenRecovery.addTokenToDataStore(budgeteerId)
                while PasswordTokenRecovery.getTokenByBudgeteerId(budgeteerId) is None:
                    time.sleep(0.5)
                MailSender.sendTokenInEmail(budgeteer.firstName, budgeteer.lastName,
                                            budgeteer.email, PasswordTokenRecovery.getTokenByBudgeteerId(budgeteerId))

                template_params['emailStatus'] = "An Email with password has already been sent."
        else:
            template_params['emailStatus'] = "There is no such email."

        html = template.render("web/templates/PasswordRecovery.html", template_params)
        self.response.write(html)


class SendNewPasswordHandler(webapp2.RequestHandler):
    def get(self, token):
        budgeteerId = PasswordTokenRecovery.resetPassword(token)
        if budgeteerId:
            budgeteer = Budgeteer.getBudgeteerById(budgeteerId)
            newPass = ''.join(string.digits[ord(c) % len(string.digits)] for c in os.urandom(16))
            MailSender.sendNewPasswordToEmail(budgeteer.firstName, budgeteer.lastName, budgeteer.email, newPass)
            budgeteer.password = newPass
            Budgeteer.updateBudgeteerAccount(budgeteer)
            self.redirect("/Login")
        else:
            self.redirect("/404")

app = webapp2.WSGIApplication([
    ('/PasswordRecovery[\/]?', IndexHandler),
    ('/PasswordRecovery/(.*)', SendNewPasswordHandler)
], debug=True)



