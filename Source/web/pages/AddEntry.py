from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer

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
        html = template.render("web/templates/add_entry.html", template_params)
        self.response.write(html)

app = webapp2.WSGIApplication([('/AddEntry', IndexHandler)], debug=True)
