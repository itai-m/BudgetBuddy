from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
from models.BudgetModel import Budget

class IndexHandler(webapp2.RequestHandler):
    def get(self,budgetId):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
            if not budgeteer:
                self.redirect('/Login')
                return
        else:
            self.redirect('/Login')
            return

        budget = Budget.getBudgetById(long(budgetId))
        template_params = dict()
        template_params['userName'] = budgeteer.userName
        template_params['budget'] = budget
        template_params['budgetId'] = budgetId
        html = template.render("web/templates/Budget.html", template_params)
        self.response.write(html)

app = webapp2.WSGIApplication([
    ('/Budget/(.*)', IndexHandler),
], debug=True)
