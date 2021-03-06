from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
from datetime import datetime
import json


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

        Email = self.request.get('email')
        UserName = self.request.get('username')
        password = self.request.get('password')
        template_params = dict()
        if Budgeteer.budgeteerUserNameExist(UserName):
            self.error(403)
            self.response.write('UserName already exists')
            return
        if Budgeteer.budgeteerEmailExist(Email):
            self.error(403)
            self.response.write('Email already exists')
            return
        if len(password) < 6:
            self.error(403)
            self.response.write('Password must be at least 6 characters')
            return
        BudgeteerObj = Budgeteer()
        BudgeteerObj.email = Email
        BudgeteerObj.userName = UserName
        BudgeteerObj.password = password

        budgeteerId = Budgeteer.registerBudgeteer(BudgeteerObj)

        if not budgeteerId:
            self.error(403)
            self.response.write('Wrong Username Or Password')
            return

        self.response.write(json.dumps({'status':'OK'}))
        self.response.set_cookie('budgeteerIdToken', str(budgeteerId))



app = webapp2.WSGIApplication([('/Registration', IndexHandler), ('/RegistrationCheck', RegistrationCheckHandler)], debug=True)
