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
        template_params['firstName'] = budgeteerId.firstName
        template_params['lastName'] = budgeteerId.lastName
        template_params['email'] = budgeteerId.email
        template_params['gender'] = budgeteerId.gender
        template_params['birthday'] = budgeteerId.birthday
        html = template.render("web/templates/profileSettings.html", template_params)
        self.response.write(html)

app = webapp2.WSGIApplication([('/ProfileSettings', IndexHandler)], debug=True)
