from google.appengine.ext import ndb
from BudgetModel import Budget
class Budgeteer(ndb.Model):
    userName = ndb.StringProperty()
    password = ndb.StringProperty()
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    email = ndb.StringProperty()
    birthday = ndb.DateProperty()
    gender = ndb.StringProperty() #char. m for male, f for female
    notifications = ndb.KeyProperty(kind='BudgeteerNotification')
    budgetsList = ndb.KeyProperty(kind='Budget',repeated=True) #list of budgets related to the user

#added budget

    @staticmethod
    def addBudgeteerAccount(budgeteerToAdd):
        if (Budgeteer.checkIfUserExists(budgeteerToAdd.userName)) is not None:
            budgeteerToAdd.put()
            return budgeteerToAdd
        else:
            return None

    @staticmethod
    def updateBudgeteerAccount(budgeteerToEdit):
        budgeteerToEdit.put()

    @staticmethod
    def checkIfUserExists(userName):
        for bgt in Budgeteer.query():
            if (bgt.userName == userName):
                return bgt
        return None

    def checkLogIn(userName,password):
        for bgt in Budgeteer.query():
            if ((bgt.userName == userName) and (bgt.password == password)):
                return bgt
        return None

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
    
