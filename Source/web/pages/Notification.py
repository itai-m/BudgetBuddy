from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
from models.BudgeteerNotificationModel import BudgeteerNotification
import json

class ShowNotificationHandler(webapp2.RequestHandler):
    def get(self):
        budgeteer_id = None
        notification_id = self.request.get("notification_id")
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

        if notification_id is None:
            self.error(200)
            return

        notification_id = long(notification_id)
        if BudgeteerNotification.get_by_id(notification_id) is None:
            self.error(200)
            return

        if BudgeteerNotification.get_by_id(notification_id).dstBudgeteer != \
                Budgeteer.getBudgeteerById(budgeteer_id).key:
            self.error(403)
            self.response.write("You Are Not Authorized to remove this Notification")
            return

        link = BudgeteerNotification.get_by_id(notification_id).link
        BudgeteerNotification.removeNotificationByKey(BudgeteerNotification.get_by_id(notification_id).key)
        self.error(200)
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.out.write(json.dumps({'link': link, 'status': 'OK'}))


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
    ('/RemoveNotification', ShowNotificationHandler),
    ('/RemoveAllNotifications', RemoveAllNotifications)
], debug=True)