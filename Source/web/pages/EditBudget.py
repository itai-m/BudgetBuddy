from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer

class IndexHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteerId = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
        else:
            self.redirect('/Login')
            return
        if not budgeteerId:
            self.redirect('/Login')
            return
        template_params = dict()
        template_params['userName'] = budgeteerId.userName
        html = template.render("web/templates/EditBudget.html", template_params)
        self.response.write(html)

app = webapp2.WSGIApplication([('/EditBudget', IndexHandler)], debug=True)
