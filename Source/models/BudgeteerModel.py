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
    budgetsList = ndb.KeyProperty(kind='Budget',repeated=True) #list of budgets related to the user
    budgeteerSettingNotifyIfAddedToBudget = ndb.BooleanProperty() #Invited to a budget
    budgeteerSettingNotifyIfChangedEntry = ndb.BooleanProperty() #Remove\Add\Change entry


    @staticmethod
    def addBudgeteerAccount(budgeteerToAdd):
        if (Budgeteer.getBudgeteer(budgeteerToAdd)) is None:
            budgeteerToAdd.put()
            return budgeteerToAdd
        else:
            return None

    @staticmethod
    def updateBudgeteerAccount(budgeteerToEdit):
        budgeteerToEdit.put()

    @staticmethod
    def getBudgeteer(budgeteerToAdd):

        if Budgeteer.getBudgeteerByEmail(budgeteerToAdd.email):
            return Budgeteer.getBudgeteerByEmail(budgeteerToAdd.email)

        elif Budgeteer.getBudgeteerByUserName(budgeteerToAdd.userName):
           return Budgeteer.getBudgeteerByUserName(budgeteerToAdd.userName)

        return None

    @staticmethod
    def getBudgeteerByUserName(userName):
        return Budgeteer.query(Budgeteer.userName==userName).get()
        pass

    @staticmethod
    def getBudgeteerByEmail(email):
        return Budgeteer.query(Budgeteer.email==email).get()
        pass


    @staticmethod
    def checkLogIn(userName,password):
        if Budgeteer.query(ndb.AND(Budgeteer.userName==userName,Budgeteer.password==password)).get():
            return True
        return False

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
        budgets = []
        for key in budgeteer.budgetList:
            budgets += Budget.budgetKeyToBudget(key)
        return budgets
    
    @staticmethod
    def getNotificationsList(budgeteer):

        notificationsList = []

        for notification in BudgeteerNotification.getNotifications():
            if budgeteer.key == notification.dst: #dst saves the destination budgeteer key
                notificationsList += notification

        return notificationsList
