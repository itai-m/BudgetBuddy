from __builtin__ import staticmethod
from google.appengine.ext import ndb
from TagModel import Tag
from EntryModel import Entry
import json

class Budget(ndb.Model):
    budgetName = ndb.StringProperty()
    creationDate = ndb.DateProperty()
    tagsList = ndb.KeyProperty(kind='Tag',repeated=True) #list of tag id
    entryList = ndb.KeyProperty(kind='Entry',repeated=True) #list of entry id
    participantsAndPermission = ndb.StringProperty(repeated=True) # "liran123":5 

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
    
    def deleteBudget(budget):
        # Delete all keys
        budget = Budget.get(budget.key)
        for entryKey in budget.entryList:
            Entry.deleteEntry(entryKey)
        # Go through all the participants and remove the key from their list (?)
        # Remove budget from datastore
        budget.key.delete()
        
            