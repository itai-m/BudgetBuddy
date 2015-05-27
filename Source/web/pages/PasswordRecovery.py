from google.appengine.ext.webapp import template
from google.appengine.api import mail
from models.BudgeteerModel import Budgeteer
import webapp2


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        template_params = {}
        html = template.render("web/templates/PasswordRecovery.html", template_params)
        self.response.write(html)

    def post(self):
        email = self.request.get("emailAddress")
        #check email validation

        template_params = dict()
        budgeteerId = Budgeteer.getBudgeteerIdByEmail(email)

        if (budgeteerId):
            #reset its password

            template_params['emailStatus'] = "An Email with password has been sent."
        else:
            template_params['emailStatus'] = "There is no such email."

        html = template.render("web/templates/PasswordRecovery.html", template_params)
        self.response.write(html)

app = webapp2.WSGIApplication([('/PasswordRecovery', IndexHandler)], debug=True)
