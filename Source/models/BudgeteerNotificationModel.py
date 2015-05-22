from google.appengine.ext import ndb

class BudgeteerNotification(ndb.Model):
    #src invited dst to share a budget
    srcBudgeteer = ndb.KeyProperty()
    dstBudgeteer = ndb.KeyProperty()
    type = ndb.StringProperty()

    @staticmethod
    def getNotificationsByDstKey(dstKey):
        '''
        Receives a budgeteer id, returns all the notifications that has the same destination ID.
        :param dstId: The Id of the destination budgeteer.
        :return: List (query) of all the destination ids that equals to the received dstId
        '''
        return BudgeteerNotification.query(BudgeteerNotification.dstBudgeteer == dstKey)

    @staticmethod
    def addNotification(budgeteerNotification):
        '''
        Gets a notification and inserts it to the datastore.
        :param budgeteerNotification: Notification object.
        :return: The notification object ID after being put in the Datastore.
        '''
        budgeteerNotification.put()
        return budgeteerNotification.key.id()
