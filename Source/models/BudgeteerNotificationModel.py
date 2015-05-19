from google.appengine.ext import ndb

class BudgeteerNotification(ndb.Model):



    @staticmethod
    def getNotificationByKey(notificationKey):
        return BudgeteerNotification.query(BudgeteerNotification.key==notificationKey).get()

