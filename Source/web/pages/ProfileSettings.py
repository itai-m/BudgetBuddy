from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
import json


class IndexHandler(webapp2.RequestHandler):

    def get(self):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
            if not budgeteer:
                self.redirect('/Login')
                return
        else:
            self.redirect('/Login')
            return
        template.register_template_library('web.templatetags.filter_app')
        template_params = dict()
        template_params['userName'] = budgeteer.userName
        template_params['email'] = budgeteer.email
        html = template.render("web/templates/profile_settings.html", template_params)
        self.response.write(html)


class ProfileSettingsCheckHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
            if not budgeteer:
                self.redirect('/Login')
                return
        else:
            self.redirect('/Login')
            return

        Email = self.request.get('email')
        password = self.request.get('password')
        if len(password) != 0:
            OldPassword = self.request.get("oldpassword")
            checkpass = Budgeteer.logIn(budgeteer.userName, OldPassword)
            if not checkpass:
                self.error(403)
                self.response.write('Old password not currect')
                return
            if len(password)<6:
                self.error(403)
                self.response.write('password must be at least 6 characters')
                return
            budgeteer.password = password
        if not (Email.lower() == budgeteer.email.lower()):
            if Budgeteer.budgeteerEmailExist(Email):
                self.error(403)
                self.response.write('Email already exists')
                return
        budgeteer.email = Email

        if len(password) != 0:
            budgeteerId = Budgeteer.updateBudgeteerAccount(budgeteer)
        else:
            budgeteerId = Budgeteer.updateBudgeteerAccount(budgeteer, False)

        if not budgeteerId:
            self.error(403)
            self.response.write('Wrong Username Or Password')
            return

        self.response.write(json.dumps({'status':'OK'}))
        self.response.set_cookie('budgeteerIdToken', str(budgeteerId))

app = webapp2.WSGIApplication([('/ProfileSettings', IndexHandler),
                               ('/ProfileSettingsCheck', ProfileSettingsCheckHandler)],
                              debug=True)
