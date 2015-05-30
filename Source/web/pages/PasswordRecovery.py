from google.appengine.ext.webapp import template
from google.appengine.api import mail
from models.BudgeteerModel import Budgeteer
from models.PasswordTokenRecoveryModel import PasswordTokenRecovery
import webapp2
import string
import os

class MailSender:
    def __init__(self):
        pass

    @staticmethod
    def sendTokenInEmail(toFirstName, toLastName, toAddress, toToken):
        body = """
        Hello,
        Please go to %s
        and then wait for your new password to be sent to your email
        """ % toToken

        mail.send_mail("BudgetBuddy Support <budgetbuddy00@gmail.com>",
                       toFirstName + " " + toLastName + " <" + toAddress + ">",
                       "Password Recovery", body)

    @staticmethod
    def sendNewPasswordToEmail(toFirstName, toLastName, toAddress, toPass):
        body = """
        Hello,
        Your new password has been set to %s
        You can login through our login http://budgetBuddy00.appspot.com/Login
        with your username and password
        """ % toPass
        mail.send_mail("BudgetBuddy Support <budgetbuddy00@gmail.com>",
                       toFirstName + " " + toLastName + " <" + toAddress + ">",
                       "Password Recovery", body)

class IndexHandler(webapp2.RequestHandler):
    def get(self):
        template_params = dict()
        html = template.render("web/templates/PasswordRecovery.html", template_params)
        self.response.write(html)

    def post(self):
        email = self.request.get("emailAddress")
        #check email validation

        template_params = dict()
        budgeteerId = Budgeteer.getBudgeteerIdByEmail(email)

        if (budgeteerId):
            budgeteer = Budgeteer.getBudgeteerById(budgeteerId)
            tokenForBudgeteerId = PasswordTokenRecovery.getTokenByBudgeteerId(budgeteerId)
            if tokenForBudgeteerId:
                template_params['emailStatus'] = "An Email with password has already been sent." + \
                                                 " Please wait couple of minutes"
            else:
                PasswordTokenRecovery.addTokenToDataStore(budgeteerId)
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
            self.redirect("/")
        else:
            self.redirect("/404")

app = webapp2.WSGIApplication([
    ('/PasswordRecovery[\/]?', IndexHandler),
    ('/PasswordRecovery/(.*)', SendNewPasswordHandler)
], debug=True)



