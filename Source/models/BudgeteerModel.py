from google.appengine.ext import ndb
from BudgeteerNotificationModel import BudgeteerNotification
from BudgetModel import Budget

class Budgeteer(ndb.Model):
    userName = ndb.StringProperty()
    password = ndb.StringProperty()
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    email = ndb.StringProperty()
    birthday = ndb.DateProperty()
    gender = ndb.StringProperty() #char. m for male, f for female
    budgetList = ndb.KeyProperty(kind='Budget',repeated=True) #list of budgets related to the user
    budgeteerSettingNotifyIfAddedToBudget = ndb.BooleanProperty() #Invited to a budget
    budgeteerSettingNotifyIfChangedEntry = ndb.BooleanProperty() #Remove\Add\Change entry


    @staticmethod
    def registerBudgeteer(budgeteer):
        budgeteer.put()
        return budgeteer
    
    @staticmethod
    def updateBudgeteerAccount(budgeteerToEdit):
        budgeteerToEdit.put()

    @staticmethod
    def budgeteerUserNameExist(userName):
        if Budgeteer.query(Budgeteer.userName==userName).get():
            return True
        return False
        
    @staticmethod
    def budgeteerEmailExist(email):
        if Budgeteer.query(Budgeteer.userName==email).get():
            return True
        return False
    
    @staticmethod
    def getBudgeteerByUserName(userName):
        return Budgeteer.query(Budgeteer.userName==userName).get()
        
    @staticmethod
    def getBudgeteerByEmail(email):
        return Budgeteer.query(Budgeteer.email==email).get()

    @staticmethod
    def logIn(userName,password):
        return Budgeteer.query(ndb.AND(Budgeteer.userName==userName,Budgeteer.password==password)).get()


    @staticmethod
    def retrievePassword(email):
        if Budgeteer.getBudgeteerByEmail(email):
            return Budgeteer.getBudgeteerByEmail(email).password
        return False

    @staticmethod
    def getBudgetList(budgeteer):
        '''
        Receives a Budgeteer object, extracts the keylist, and converts it to a Budget object list.
    
        IN: budgeteer - Budgeteer object
        OUT: Budget object list
        '''
        budgetList = []
        for singleBudget in Budgeteer.query(Budgeteer.key==budgeteer.key):
            for budgetKey in singleBudget.budgetList:
                budgetList += Budgeteer.getBudgetByKey(budgetKey)
        return budgetList

    
    @staticmethod
    def getNotificationsList(budgeteer):

        notificationsList = []

        for notification in BudgeteerNotification.getNotifications():
            if budgeteer.key == notification.dst: #dst saves the destination budgeteer key
                notificationsList += notification

        return notificationsList

    @staticmethod
    def addBudgetToBudgetList(budgeteer,budget):

        budgetList = Budgeteer.getBudgetList(budgeteer)
        budgetList.append(budget.key)
        budgeteer.budgetList=budgetList
        budgeteer.put()

    @staticmethod
    def getBudgeteerByKey(budgeteerKey):
        return Budgeteer.query(Budgeteer.key==budgeteerKey)
