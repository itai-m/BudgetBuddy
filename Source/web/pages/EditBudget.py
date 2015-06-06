from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
from models.BudgetModel import Budget

class EditBudgetHandler(webapp2.RequestHandler):
    def get(self,budgetId):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
        else:
            self.redirect('/Login')
            return
        if not budgeteer:
            self.redirect('/Login')
            return
        template_params = dict()
        budget=Budget.getBudgetById(long(budgetId))

        template_params['userName'] = budgeteer.userName
        template_params['budgetName'] = budget.budgetName


        html = template.render("web/templates/EditBudget.html", template_params)
        self.response.write(html)

app = webapp2.WSGIApplication([('/EditBudget/(.*)', EditBudgetHandler)], debug=True)
