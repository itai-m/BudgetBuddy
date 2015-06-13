from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer

class HelpHandler(webapp2.RequestHandler):
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
            template_params['userName'] = budgeteer.userName
            template.register_template_library('web.templatetags.filter_app')
        else:
            template_params['base_template'] = "guest_master.html"

        html = template.render("web/templates/help.html", template_params)
        self.response.write(html)

app = webapp2.WSGIApplication([('/Help', HelpHandler)], debug=True)
