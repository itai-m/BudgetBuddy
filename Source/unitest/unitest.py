from google.appengine.ext import ndb
import json
from datetime import datetime

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
class Tag(ndb.Model):
    description = ndb.StringProperty()


    @staticmethod
    def getTagDesc(tagKey):
        return Tag.query(Tag.key == tagKey)
class BudgeteerPermission(ndb.Model):
    permissionName = ndb.StringProperty()
    permissionLevel = ndb.IntegerProperty()
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

    @staticmethod
    def addBudgetToBudgetList(budgeteer,budget):

        budgetList = Budgeteer.getBudgetList(budgeteer)
        budgetList.append(budget.key)
        budgeteer.budgetList=budgetList
        budgeteer.put()

    @staticmethod
    def getBudgeteerByKey(budgeteerKey):
        return Budgeteer.query(Budgeteer.key==budgeteerKey)
class Budget(ndb.Model):
    budgetName = ndb.StringProperty()
    creationDate = ndb.DateProperty()
    tagsList = ndb.KeyProperty(kind='Tag',repeated=True) #list of tag id
    entryList = ndb.KeyProperty(kind='Entry',repeated=True) #list of entry id
    participantsAndPermission = ndb.StringProperty(repeated=True) # "liran123":5


    @staticmethod
    def addBudget(budget):
        budget.put()
        budgetKey= budget.key
        Budget.addBudgetToBudgeteers(budget)

    @staticmethod
    def addBudgetToBudgeteers(budget):
        participantsDict=Budget.getParticipantsAndPermissionsDict(budget)
        for budgeteerKey in participantsDict.keys():
            bgt = Budgeteer.getBudgeteerByKey(budgeteerKey)
            Budgeteer.addBudgetToBudgetList(bgt,budget)


    @staticmethod
    def budgetKeyToBudget(budgetKey):
        return Budget.query(Budget.key == budgetKey)

    def getTagList(budget):
        '''
        Receives a Budget object, and extracts the tags associated with it

        IN: Budget object
        OUT: List of tag strings
        '''
        tagList = []
        for singleBudget in Budget.query(Budget.key==budget.key):
            for tagKey in singleBudget.tagsList:
                tagList += Tag.getTagDesc(tagKey)

        return tagList

    @staticmethod
    def addEntryToBudget(entry,budget):
        #checked
        entryKey = Entry.addEntry(entry)
        entryListToAddTheKey = Budget.getEntryList(budget)
        entryListToAddTheKey.append(entryKey)
        budget.entryList = entryListToAddTheKey
        budget.put()


    def getEntryList(budget):
        '''
        Receives a Budget object, and extracts the entries associated with it

        IN: Budget object
        OUT: List of Entry objects
        '''
        entryList = []
        for singleBudget in Budget.query(Budget.key==budget.key):
            for entryKey in singleBudget.entryList:
                entryList += Entry.getEntry(entryKey)

        return entryList

    def getParticipantsAndPermissionsDict(budget):
        partAndPermDict = {}
        for singleBudget in Budget.query(Budget.key==budget.key):
            for entry in singleBudget.participantsAndPermission:
                partAndPermDict.update(dict(json.loads(entry)))
        return partAndPermDict
class Entry(ndb.Model):
    description = ndb.StringProperty()
    amount = ndb.FloatProperty()
    addedBy = ndb.KeyProperty()
    creationDate = ndb.DateProperty()
    tagId = ndb.KeyProperty()

    @staticmethod
    def addEntry(entry):
        entry.put()
        return entry.key
    @staticmethod
    def getEntry(entryKey):
        return Entry.query(Entry.key == entryKey)

##Add Budgeteer at initial
rotem = Budgeteer(userName = "rotem1111",password="123123",firstName="Rotem",
                  lastName="ne",email="ro@ro.com",birthday=datetime.now(),
                  gender="f",budgeteerSettingNotifyIfAddedToBudget=True,budgeteerSettingNotifyIfChangedEntry=True,budgetsList =())
#Store bugeteer in datastore
rotem.put()
print "Added Budgeteer: " + rotem.firstName
#Add Budget


alist = []
alist.append(json.dumps({ "R0tem" : "Manager" })) #set permissionList

tgs = Tag(description="Salad")
tgs.put()
etry = Entry(description="hummos",amount=5.5,addedBy=rotem.key,creationDate=datetime.now(),tagId=tgs.key)

bgt = Budget(budgetName="BRBQ",creationDate=datetime.now(),tagsList=(),entryList=(),participantsAndPermission=alist)
Budget.addBudget(bgt)
Budget.addEntryToBudget(etry,bgt)

print "ok"
"""
for remove in Budget.query():
    remove.key.delete()
for remove in Budgeteer.query():
    remove.key.delete()
for remove in Entry.query():
    remove.key.delete()
for remove in Tag.query():
    remove.key.delete()
"""
