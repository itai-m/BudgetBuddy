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
        template_params['NotificationList'] = notifications
        template_params['userName'] = budgeteer.userName
        html = template.render("web/templates/notifications.html", template_params)

        self.response.write(html)


class ReadNotificationHandler(webapp2.RequestHandler):
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

        if self.request.get("notification_id") is None or self.request.get("notification_id") == '':
            self.error(403)
            return

        notification_id = long(self.request.get("notification_id"))

        if notification_id is None:
            self.error(403)
            return

        notification = BudgeteerNotification.get_by_id(notification_id)

        if notification is None:
            self.error(403)
            return

        if notification.dstBudgeteer !=  Budgeteer.getBudgeteerById(budgeteer_id).key:
            self.error(403)
            self.response.write("You Are Not Authorized to remove this Notification")
            return

        BudgeteerNotification.setReadNotification(notification.key)
        notifications = BudgeteerNotification.getUnreadNotificationsByDstKey(budgeteer.key)
        template.register_template_library('web.templatetags.filter_app')

        list_to_write = []
        for notification_in_list in notifications:
            list_to_write.append({"message":notification_in_list.message })
        self.error(200)
        self.response.write(json.dumps(
            {
                'link': notification.link,
                'notifications':list_to_write,
                'status':'OK'
            }
        ))


class MarkAllAsReadHandler(webapp2.RequestHandler):
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
        notificationsList = Budgeteer.getNotificationList(budgeteer)
        for notification in notificationsList:
            if notification.read == False:
                BudgeteerNotification.setReadNotification(notification.key)
        self.error(200)
        self.response.write(json.dumps({'status':'OK'}))


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


class GetAllNotificationsHandler(webapp2.RequestHandler):
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
        notifications = BudgeteerNotification.getUnreadNotificationsByDstKey(budgeteer.key)
        if len(notifications) == 0:
            self.error(200)
            self.response.write(json.dumps({'status': 'OK'}))

        list_to_write = []
        for notification in notifications:
            list_to_write.append({'message':notification.message,'id':notification.key.id()})

        self.error(200)
        self.response.write(
            json.dumps(

                {'notifications': list_to_write},
                {'status': 'OK'}
            )
        )

app = webapp2.WSGIApplication([
    ('/ShowNotifications', ShowNotificationHandler),
    ('/RemoveAllNotifications', RemoveAllNotifications),
    ('/ReadNotification', ReadNotificationHandler),
    ('/MarkAllAsRead', MarkAllAsReadHandler),
    ('/GetAllNotification', GetAllNotificationsHandler)
], debug=True)
