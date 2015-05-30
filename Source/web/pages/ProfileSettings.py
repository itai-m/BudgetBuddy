from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
import calendar
register = template.django.template.Library()


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

        template_params = dict()
        template_params['userName'] = budgeteer.userName
        template_params['firstName'] = budgeteer.firstName
        template_params['lastName'] = budgeteer.lastName
        template_params['email'] = budgeteer.email
        template_params['gender'] = budgeteer.gender
        template_params['birthday'] = budgeteer.birthday
        html = template.render("web/templates/profileSettings.html", template_params)
        self.response.write(html)

@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]

app = webapp2.WSGIApplication([('/ProfileSettings', IndexHandler)], debug=True)
