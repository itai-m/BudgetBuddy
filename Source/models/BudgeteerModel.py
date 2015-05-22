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
        '''
        This function assumes that the Username and Email provided in the budgeteer object does not already exist.
        :param budgeteer: Budgeteer object, contains all the budgeteer information needed to register
                          budgeteer, such as name, username, password, email, birthday, notification settings.
        :return: returns the budgeteer key id.
        '''
        budgeteer.put()
        return budgeteer.key.id()
    
    @staticmethod
    def updateBudgeteerAccount(budgeteerToEdit):
        '''
        Receives a budgeteer and replaces the current object data with the received data.
        (Identical to Register budgteer function)
        :param budgeteerToEdit: Budgeteer object that contains all the budgeteer updated data.
        :return: budgeteer key id.
        '''
        budgeteerToEdit.put()
        return budgeteerToEdit().key.id()

    @staticmethod
    def budgeteerUserNameExist(userName):
        '''
        Validator function for the Registration procedure.
        :param userName: string contains the username.
        :return: Boolean variable, True if username exists, false if not.
        '''
        if Budgeteer.query(Budgeteer.userName == userName).get():
            return True
        return False
        
    @staticmethod
    def budgeteerEmailExist(email):
        '''
        Validator function for the Registration procedure.
        :param email: string contains the email.
        :return: Boolean variable, True if email exists, false if not.
        '''
        if Budgeteer.query(Budgeteer.userName == email).get():
            return True
        return False
    
    @staticmethod
    def getBudgeteerIdByUserName(userName):
        '''
        Converts userName to budgeteer ID.
        :param userName: The budgeteer username string.
        :return: budgeteer key id.
        '''
        return Budgeteer.query(Budgeteer.userName == userName).get().key.id()
        
    @staticmethod
    def getBudgeteerByEmail(email):
        '''
        Converts email to budgeteer.
        :param email: The budgeteer email string.
        :return: budgeteer object if email exist, None if not.
        '''
        return Budgeteer.query(Budgeteer.email == email).get()

    @staticmethod
    def logIn(userName,password):
        '''
        Compares the budgeteer password and budgeteer username against the datastore.
        :param userName: budgeteer username.
        :param password: budgeteer password.
        :return: None if the username-password combination is not found.
                 Budgeteer key id if the combination is found.
        '''
        return Budgeteer.query(ndb.AND(Budgeteer.userName == userName, Budgeteer.password == password)).get().key.id()

    @staticmethod
    def retrievePassword(email):
        '''
        Given an email string, returns the password string.
        :param email: Email string.
        :return: Password associated with the email if exists, None if not.
        '''
        budgeteer = Budgeteer.getBudgeteerByEmail(email)
        if budgeteer:
            return budgeteer.password
        return None

    @staticmethod
    def getBudgetList(budgeteer):
        '''
        :param budgeteer: Budgeteer object.
        :return: List of Budget objects.
        '''
        budgetList = []
        for budgetKey in budgeteer.budgetList:
            budgetList.append(Budget.getBudgetByKey(budgetKey).id())
        return budgetList
    
    @staticmethod
    def getNotificationsList(budgeteer):
        '''
        Receives a budgeteer, returns a Notification object list associated with that budgeteer.
        :param budgeteer: Budgeteer object.
        :return: list of Notification objects associated with the budgeteer given.
        '''
        notificationsList = []
        for notification in BudgeteerNotification.getNotifications():
            if budgeteer.key.id() == notification.dst:
                notificationsList.append(notification)
        return notificationsList

    @staticmethod
    def addBudgetToBudgetList(budgeteer,budget):
        '''
        Adds a budget to the budgeteer budgetList.
        :param budgeteer: Budgeteer object, append the budget id to this budgeteer.budgetList.
        :param budget: take this budget.key.id() and add to the budgeteer.budgetList.
        :return: budgeteer.key.id().
        '''
        budgeteer.budgetList.append(budget.key.id())
        budgeteer.put()
        return budgeteer.key.id()

    @staticmethod
    def getBudgeteerByKey(budgeteerId):
        '''
        Converts a budgeteer ID to a budgeteer object.
        :param budgeteerKey: budgeteer id.
        :return: budgeteer object associated with that id.
        '''
        return Budgeteer.query(Budgeteer.key.id() == budgeteerId).get()