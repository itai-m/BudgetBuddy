from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.cookies.get('budgeteerIdToken'):    #the cookie that should contain the access token!
            budgeteer = Budgeteer.getBudgeteerById(self.request.cookies.get('budgeteerIdToken'))
            if budgeteer:
                self.redirect('/Budgets')

        template_params = dict()
        html = template.render("web/templates/registration.html", template_params)
        self.response.write(html)

class RegistrationCheckHandler(webapp2.RequestHandler):

    def get(self):
        firstname = self.request.get('FirstName')
        lastname = self.request.get('LastName')
        email = self.request.get('email')
        username = self.request.get('username')
        password = self.request.get('password')
        budgeteerId = Budgeteer.logIn(username, password)

        if not budgeteerId :
            self.error(403)
            self.response.write('Wrong Username Or Password')
            return

        self.response.set_cookie('budgeteerIdToken', str(budgeteerId))


app = webapp2.WSGIApplication([('/Registration', IndexHandler), ('/RegistrationCheck', RegistrationCheckHandler)], debug=True)
