from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer

class AboutUsHandler(webapp2.RequestHandler):
    def get(self):
        template_params = {}
        loggedIn = True
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
            if not budgeteer:
                loggedIn = False
        else:
                loggedIn = False
        
        if loggedIn:
            template_params['base_template'] = "master_page.html"
        else:
            template_params['base_template'] = "guest_master.html"

        html = template.render("web/templates/AboutUs.html", template_params)
        self.response.write(html)

app = webapp2.WSGIApplication([('/AboutUs', AboutUsHandler)], debug=True)
