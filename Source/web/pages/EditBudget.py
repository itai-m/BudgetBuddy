from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer

class EditBudgetHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
        else:
            self.redirect('/Login')
            return
        if not budgeteer:
            self.redirect('/Login')
            return
        template_params = dict()
        template.register_template_library('web.templatetags.filter_app')
        template_params['userName'] = budgeteer.userName
        html = template.render("web/templates/EditBudget.html", template_params)
        self.response.write(html)

app = webapp2.WSGIApplication([('/EditBudget', EditBudgetHandler)], debug=True)
