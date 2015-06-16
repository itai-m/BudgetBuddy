from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
from models.BudgeteerNotificationModel import BudgeteerNotification
import json

class ShowNotificationHandler(webapp2.RequestHandler):
    def get(self):
        budgeteer_id = None
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer_id = long(self.request.cookies.get('budgeteerIdToken'))
            budgeteer = Budgeteer.getBudgeteerById(budgeteer_id)
            if not budgeteer:
                self.error(404)
                self.redirect('/Login')
                return
        else:
            self.error(403)
            self.redirect('/Login')
            return

        notifications = BudgeteerNotification.getNotificationsByDstKey(budgeteer.key)
        template.register_template_library('web.templatetags.filter_app')
        template_params = dict()
        template_params['notifications'] = notifications
        template_params['userName'] = budgeteer.userName
        html = template.render("web/templates/notifications.html", template_params)

        self.response.write(html)


class RemoveAllNotifications(webapp2.RequestHandler):
    def get(self):
        budgeteer_id = None
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer_id = long(self.request.cookies.get('budgeteerIdToken'))
            budgeteer = Budgeteer.getBudgeteerById(budgeteer_id)
            if not budgeteer:
                self.error(404)
                self.redirect('/Login')
                return
        else:
            self.error(403)
            self.redirect('/Login')
            return
        budgeteer = Budgeteer.getBudgeteerById(budgeteer_id)
        BudgeteerNotification.removeAllMyNotifications(budgeteer.key)
        self.error(200)
        self.response.write(json.dumps({'status': 'OK'}))


app = webapp2.WSGIApplication([
    ('/ShowNotifications', ShowNotificationHandler),
    ('/RemoveAllNotifications', RemoveAllNotifications)
], debug=True)
