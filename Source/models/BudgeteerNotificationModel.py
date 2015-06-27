from google.appengine.ext import ndb

class BudgeteerNotification(ndb.Model):
    srcBudgeteer = ndb.KeyProperty()
    dstBudgeteer = ndb.KeyProperty()
    message = ndb.StringProperty()
    link = ndb.StringProperty()
    read = ndb.BooleanProperty()

    @staticmethod
    def getNotificationsByDstKey(dstKey):
        '''
        Receives a budgeteer id, returns all the notifications that has the same destination ID.
        :param dstKey: The Id of the destination budgeteer.
        :return: List (query) of all the Budgeteer (DstKey) notification that equals to the received dstKey
        '''
        notification_list = list()
        for notification in BudgeteerNotification.query(BudgeteerNotification.dstBudgeteer == dstKey):
            notification_list.append(notification)
        return notification_list

    @staticmethod
    def getUnreadNotificationsByDstKey(dstKey):
        '''
        Receives a budgeteer id, returns all the unread notifications that has the same destination ID.
        :param dstKey: The Id of the destination budgeteer.
        :return: List (query) of all the Budgeteer (DstKey) unread notification that equals to the received dstKey
        '''
        notification_list = list()
        for notification in BudgeteerNotification.query(BudgeteerNotification.read == False, BudgeteerNotification.dstBudgeteer == dstKey):
            notification_list.append(notification)
        return notification_list

    @staticmethod
    def setReadNotification(budgeteer_notification_key):
        '''
        this function set the notification as read
        :param budgeteer_notification_key: the notification's key to change
        :return: notification read field
        '''
        notification = BudgeteerNotification.get_by_id(budgeteer_notification_key.id())
        notification.read = True
        notification.put()
        return notification.read

    @staticmethod
    def addNotification(budgeteerNotification):
        '''
        Gets a notification and inserts it to the datastore.
        :param budgeteerNotification: Notification object.
        :return: The notification object ID after being put in the Datastore.
        '''
        budgeteerNotification.put()
        return budgeteerNotification.key.id()

    @staticmethod
    def removeNotificationByKey(budgeteer_notification_key):
        '''
        Gets a notification key and removes it from the datastore
        :param budgeteerNotification: notification to remove
        :return: None
        '''
        budgeteer_notification_key.delete()
        return None

    @staticmethod
    def removeAllMyNotifications(budgeteer_dst_key):
        '''
        gets budgeteer key and removes all his notification (aka clear his list)
        :param budgeteer_dst_key: budgeteer key
        :return: None
        '''
        for notification in BudgeteerNotification.query(BudgeteerNotification.dstBudgeteer == budgeteer_dst_key):
            BudgeteerNotification.removeNotificationByKey(notification.key)
        return None
