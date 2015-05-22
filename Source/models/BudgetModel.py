from google.appengine.ext import ndb
from TagModel import Tag
from EntryModel import Entry
from BudgeteerModel import Budgeteer
import json

class Budget(ndb.Model):
    budgetName = ndb.StringProperty()
    creationDate = ndb.DateProperty()
    tagsList = ndb.KeyProperty(kind='Tag',repeated=True) #list of tag id
    entryList = ndb.KeyProperty(kind='Entry',repeated=True) #list of limited available tags. decided by manager
    participantsAndPermission = ndb.StringProperty(repeated=True) # "liranObjectKey":"Manager"


    @staticmethod
    def addBudget(budget):
        budget.put()
        Budget.addBudgetToBudgeteers(budget)

    @staticmethod
    def addBudgetToBudgeteers(budget):
        participantsDict=Budget.getParticipantsAndPermissionsDict(budget)
        for budgeteerKey in participantsDict.keys():
            bgt = Budgeteer.getBudgeteerByKey(budgeteerKey)
            Budgeteer.addBudgetToBudgetList(bgt,budget)

    @staticmethod
    def getBudgetByKey(budgetKey):
        return Budget.query(Budget.key == budgetKey).get()

    def getTagList(budget):
        '''
        Receives a Budget object, and extracts the tags associated with it
        
        IN: Budget object
        OUT: List of tag strings
        '''
        tagList = []
        for singleBudget in Budget.query(Budget.key==budget.key):
            for tagKey in singleBudget.tagsList:
                tagList.append(Tag.getTag(tagKey))
        return tagList

    @staticmethod
    def addEntryToBudget(entry,budget):
        #checked
        entryKey = Entry.addEntry(entry)
        entryListToAddTheKey = Budget.getEntryList(budget)
        entryListToAddTheKey.append(entryKey)
        budget.entryList = entryListToAddTheKey
        budget.put()

    @staticmethod
    def getEntryList(budget):
        '''
        Receives a Budget object, and extracts the entries associated with it
        
        IN: Budget object
        OUT: List of Entry objects
        '''
        entryList = []
        for singleBudget in Budget.query(Budget.key==budget.key):
            for entryKey in singleBudget.entryList:
                entryList.append(Entry.getEntryByKey(entryKey))
        return entryList
    @staticmethod
    def getParticipantsAndPermissionsDict(budget):
        partAndPermDict = {}
        for singleBudget in Budget.query(Budget.key==budget.key):
            for entry in singleBudget.participantsAndPermission:
                partAndPermDict.update(dict(json.loads(entry)))
        return partAndPermDict
    @staticmethod
    def deleteBudget(budget):
        # Delete all keys
        budgetToDelete = Budget.query(Budget.key==budget.key).get()
        for entryKey in budget.entryList:
            Entry.deleteEntry(entryKey)
        # Go through all the participants and remove the key from their list (?)
        # Remove budget from datastore
        budgetToDelete.key.delete()
    @staticmethod
    def addTagToBudget(tag,budget):       
        tagListToAddTheKey = Budget.getTagList(tag)
        tagListToAddTheKey.append(tag.key)
        budget.tagList = tagListToAddTheKey
        budget.put()
