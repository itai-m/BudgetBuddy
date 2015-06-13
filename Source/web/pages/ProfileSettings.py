from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
import calendar
register = template.django.template.Library()
from datetime import datetime
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
        template_params['firstName'] = budgeteer.firstName
        template_params['lastName'] = budgeteer.lastName
        template_params['email'] = budgeteer.email
        template_params['gender'] = budgeteer.gender
        template_params['birthday'] = budgeteer.birthday
        html = template.render("web/templates/profile_settings.html", template_params)
        self.response.write(html)


@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]


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
        BirthYear = self.request.get("BirthYear")
        password = self.request.get('password')
        if len(password) != 0:
            OldPassword = self.request.get("oldpassword")
            checkpass = Budgeteer.logIn(budgeteer.userName, OldPassword)
            if not checkpass:
                self.response.write('Old password not currect')
                return
            if len(password)<6:
                self.response.write('password must be at least 6')
                return
            budgeteer.password = password
        if not (Email.lower() == budgeteer.email.lower()):
            if Budgeteer.budgeteerEmailExist(Email):
                self.response.write('Email already exists')
                return
        if int(BirthYear) < 1900:
            self.response.write('Year of birth is not valid')
            return
        budgeteer.email = Email
        budgeteer.firstName = self.request.get('FirstName')
        budgeteer.lastName = self.request.get('LastName')
        BirthMonth = self.request.get("BirthMonth")
        BirthMonth = BirthMonth.zfill(2)
        BirthDay = self.request.get("BirthDay")
        BirthDay = BirthDay.zfill(2)
        try:
            budgeteer.birthday = datetime.strptime('' + BirthDay + ' ' + BirthMonth + ' ' + BirthYear, '%d %m %Y')
        except ValueError:
            self.response.write('Wrong Date Input')
            return
        budgeteer.gender = self.request.get("gender")

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
