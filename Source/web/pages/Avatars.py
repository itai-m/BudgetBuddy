from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer

class AvatarsHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
        else:
            self.redirect('/Login')
            return
        if not budgeteer:
            self.redirect('/Login')
            return

        template.register_template_library('web.templatetags.filter_app')
        template_params = {}
        template_params['userName'] = budgeteer.userName

        html = template.render("web/templates/avatars.html", template_params)
        self.response.write(html)

class ChangeAvatarHandler(webapp2.RequestHandler):
    def get(self, avatarId):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
        else:
            self.redirect('/Login')
            return
        if not budgeteer:
            self.redirect('/Login')
            return
        budgeteer.avatar = int(avatarId)
        budgeteer.put()     
        template.register_template_library('web.templatetags.filter_app')
        template_params = {}
        template_params['userName'] = budgeteer.userName

        html = template.render("web/templates/avatars.html", template_params)
        self.response.write(html)


app = webapp2.WSGIApplication([('/Avatars', AvatarsHandler),
                               ('/ChangeAvatar/(.*)', ChangeAvatarHandler)],
                               debug=True)
