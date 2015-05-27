from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
import json



class IndexHandler(webapp2.RequestHandler):

    def get(self):

        budgeteerId = None
        if self.request.cookies.get('budgeteerIdToken'):    #the cookie that should contain the access token!
            budgeteerId = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
            if budgeteerId:
                return
                #self.redirect('/Budgets')

        template_params = {}
        html = template.render("web/templates/login.html", template_params)
        self.response.write(html)

class LoginCheckHandler(webapp2.RequestHandler):

    def get(self):
        username = self.request.get('username')
        password = self.request.get('password')
        budgeteerId = Budgeteer.logIn(username, password)

        if not budgeteerId :
            self.error(403)
            self.response.write('Wrong Username Or Password')
            return

        self.response.set_cookie('budgeteerIdToken', str(budgeteerId))


class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.cookies.get('budgeteerIdToken'):
                self.response.delete_cookie('budgeteerIdToken')
        self.redirect('/Login')

app = webapp2.WSGIApplication([
    ('/Login', IndexHandler),
    ('/LoginCheck', LoginCheckHandler),
    ('/Logout', LogoutHandler)
], debug=True)