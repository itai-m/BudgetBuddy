from google.appengine.ext import ndb
import BudgeteerNotificationModel
import BudgetModel
import hashlib
import operator
'''
    Functionality tests:
        [X] Username Exist
        [X] Email Exist
        [X] Get Budgeteer by Email
        [X] Get BudgeteerID By Username
        [X] Get Budgeteer By BudegteerID
        [X] Register a Budgeteer
        [X] Update Budgeteer
        [X] Login
        [X] Get Budget List
        [X] Get Notification List
        [X] Add Budget To Budget List
        [X] Remove Budget By Key
'''
class Budgeteer(ndb.Model):
    userName = ndb.StringProperty()
    password = ndb.StringProperty()
    email = ndb.StringProperty()
    avatar = ndb.IntegerProperty()
    budgetList = ndb.KeyProperty(kind=BudgetModel.Budget, repeated=True)  # list of budgets related to the user

    @staticmethod
    def registerBudgeteer(budgeteer):
        '''
        This function assumes that the Username and Email provided in the budgeteer object does not already exist.
        :param budgeteer: Budgeteer object, contains all the budgeteer information needed to register
                          budgeteer, such as name, username, password, email, birthday, notification settings.
        :return: returns the budgeteer key id.
        '''
        m = hashlib.md5()
        m.update(budgeteer.password)
        budgeteer.password = m.digest().decode("iso-8859-1")
        budgeteer.email = budgeteer.email.lower()
        budgeteer.userName = budgeteer.userName.lower()
        budgeteer.avatar = 1;
        budgeteer.put()
        return budgeteer.key.id()

    @staticmethod
    def updateBudgeteerAccount(budgeteerToEdit, newPassword = True):
        '''
        Receives a budgeteer and replaces the current object data with the received data.
        (Identical to Register budgeteer function)
        :param budgeteerToEdit: Budgeteer object that contains all the budgeteer updated data.
        :return: budgeteer key id.
        '''
        if newPassword:
            m = hashlib.md5()
            m.update(budgeteerToEdit.password)
            budgeteerToEdit.password = m.digest().decode("iso-8859-1")
        budgeteerToEdit.email.lower()
        budgeteerToEdit.userName.lower()
        budgeteerToEdit.put()
        return budgeteerToEdit.key.id()

    @staticmethod
    def budgeteerUserNameExist(userName):
        '''
        Validator function for the Registration procedure.
        :param userName: string contains the username.
        :return: Boolean variable, True if username exists, false if not.
        '''
        userName = userName.lower()
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
        email = email.lower()
        if Budgeteer.query(Budgeteer.email == email).get():
            return True
        return False
    
    @staticmethod
    def getBudgeteerIdByUserName(userName):
        '''
        Converts userName to budgeteer ID.
        :param userName: The budgeteer username string.
        :return: budgeteer key id.
        '''
        userName = userName.lower()
        budgeteerToReturn = Budgeteer.query(Budgeteer.userName == userName).get()
        if budgeteerToReturn:
            return budgeteerToReturn.key.id()
        return None
        
    @staticmethod
    def getBudgeteerIdByEmail(email):
        '''
        Converts email to budgeteer.
        :param email: The budgeteer email string.
        :return: budgeteer object id if email exist, None if not.
        '''
        email = email.lower()
        budgeteerToReturn = Budgeteer.query(Budgeteer.email == email).get()
        if budgeteerToReturn:
            return budgeteerToReturn.key.id()
        return None

    @staticmethod
    def logIn(userName,password):
        '''
        Compares the budgeteer password and budgeteer username against the datastore.
        :param userName: budgeteer username.
        :param password: budgeteer password.
        :return: None if the username-password combination is not found.
                 Budgeteer key id if the combination is found.
        '''
        userName = userName.lower()
        m = hashlib.md5()
        m.update(password)
        password = m.digest().decode("iso-8859-1")
        budgeteerToReturn = Budgeteer.query(ndb.AND(Budgeteer.userName == userName, Budgeteer.password == password)).get()
        if budgeteerToReturn:
            return budgeteerToReturn.key.id()
        return None

    @staticmethod
    def retrievePassword(email):
        '''
        Given an email string, returns the password string.
        :param email: Email string.
        :return: Password associated with the email if exists, None if not.
        '''
        email = email.lower()
        budgeteer = Budgeteer.getBudgeteerIdByEmail(email)
        if budgeteer:
            return Budgeteer.get_by_id(budgeteer).password
        return None

    @staticmethod
    def getBudgetList(budgeteer, sort_by="name", reverse=True):
        '''
        :param budgeteer: Budgeteer object.
        :return: List of Budget objects.
        '''
        budgetList = []
        for budgetKey in budgeteer.budgetList:
            budgetList.append(BudgetModel.Budget.getBudgetById(budgetKey.id()))
        if sort_by == "name":
            budgetList.sort(key=lambda x: x.budgetName, reverse=reverse)
        elif sort_by == "shared_with":
            budgetList.sort(key=lambda x: len(x.participantsAndPermission), reverse=reverse)
        elif sort_by == "creation_date":
            budgetList.sort(key=lambda x: x.creationDate, reverse=reverse)
        elif sort_by == "permission":
            # Did some nasty thing here, but couldn't think of any other way.
            # If anyone has a better idea how to sort the list by the budgeteer permission you can replace this
            budgeteer_id_string =  '{"' + str(budgeteer.key.id()) + '"'
            budgetList.sort(key=lambda x: [i for i in x.participantsAndPermission if i.split(":")[0] == budgeteer_id_string][0], reverse=reverse)
        return budgetList
    
    @staticmethod
    def getNotificationList(budgeteer):
        '''
        Receives a budgeteer, returns a Notification object list associated with that budgeteer.
        :param budgeteer: Budgeteer object.
        :return: list of Notification objects associated with the budgeteer given.
        '''
        notificationList = []
        for notification in BudgeteerNotificationModel.BudgeteerNotification.getNotificationsByDstKey(budgeteer.key):
                notificationList.append(notification)
        return notificationList

    @staticmethod
    def addBudgetToBudgetList(budgeteer, budget):
        '''
        Adds a budget to the budgeteer budgetList.
        :param budgeteer: Budgeteer object, append the budget id to this budgeteer.budgetList.
        :param budget: take this budget.key and add to the budgeteer.budgetList.
        :return: budgeteer.key.id().
        '''
        budgeteer.budgetList.append(budget.key)
        budgeteer.put()
        return budgeteer.key.id()

    @staticmethod
    def getBudgeteerById(budgeteerId):
        '''
        Converts a budgeteer ID to a budgeteer object.
        :param budgeteerID: budgeteer id.
        :return: budgeteer object associated with that id.
        '''
        return Budgeteer.get_by_id(long(budgeteerId))

    @staticmethod
    def getBudgeteerByKey(budgeteer_key):
        '''
        Converts a budgeteer ID to a budgeteer object.
        :param budgeteerID: budgeteer id.
        :return: budgeteer object associated with that id.
        '''
        return budgeteer_key.get()

    @staticmethod
    def removeBudgetByKey(participantId, budgetKey):
        '''
        Removes budget key from the budget list.
        :param particpantId: the Id of the budgeteer whose list we gonna modify.
        :param budgetKey: The key of the budget to remove.
        :return: budgeteer id.
        '''
        budgeteer = Budgeteer.getBudgeteerById(participantId)
        budgeteer.budgetList.remove(budgetKey)
        budgeteer.put()
        return budgeteer.key.id()
