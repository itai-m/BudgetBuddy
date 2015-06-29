from google.appengine.ext.webapp import template
from models.BudgeteerModel import Budgeteer
from api.MailSender import MailSender
import webapp2


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
        if not budgeteer:
            self.redirect('/Login')
        template_params = dict()
        template_params['userName'] = budgeteer.userName
        template.register_template_library('web.templatetags.filter_app')
        html = template.render("web/templates/invite_friend.html", template_params)
        self.response.write(html)

    def post(self):
        budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
        if not budgeteer:
            self.redirect('/Login')
        template.register_template_library('web.templatetags.filter_app')
        email = self.request.get("emailAddress")
        template_params = dict()
        template_params['userName'] = budgeteer.userName
        budgeteerCheck = Budgeteer.getBudgeteerIdByEmail(email)
        if budgeteerCheck:
            template_params['emailStatus'] = "There is a budgeteer with that mail"
            html = template.render("web/templates/invite_friend.html", template_params)
            self.response.write(html)
            return

        if not MailSender.check_if_email_valid(email):
            template_params['emailStatus'] = "Please insert your friend email address"
            html = template.render("web/templates/invite_friend.html", template_params)
            self.response.write(html)
            return

        MailSender.send_invite_friend(budgeteer.userName, email)
        template_params['emailStatus'] = "An Email with invitation has been sent to your friend."

        html = template.render("web/templates/invite_friend.html", template_params)
        self.response.write(html)


app = webapp2.WSGIApplication([
    ('/InviteFriend[\/]?', IndexHandler),
    ('/InviteFriend', IndexHandler)
], debug=True)
