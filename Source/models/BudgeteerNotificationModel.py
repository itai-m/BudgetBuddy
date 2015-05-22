from google.appengine.ext import ndb

class BudgeteerNotification(ndb.Model):

    #src invited dst to share a budget
    srcBudgeteer = ndb.KeyProperty()
    dstBudgeteer = ndb.KeyProperty()
    type = ndb.StringProperty()

    @staticmethod
    def getNotifications():
        return BudgeteerNotification.query()


    @staticmethod
    def notificationToDict(notificationDstKey):
        notification = BudgeteerNotification.query(BudgeteerNotification.key==notificationDstKey).get()
        if notification:
            p = {
                "src" : notification.srcBudgeteer,
                "dst" : notification.dstBudgeteer,
                "type" : notification.type
            }
            return p
        return None
    
    @staticmethod
    def addNotification(budgeteerNotification):
        budgeteerNotification.put()
