from google.appengine.ext import ndb
from TagModel import Tag
import json

class Budget(ndb.Model):
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
        for tagKey in budget.tagsList:
            tagList += Tag.getTagDesc(tagKey)
        return tagList
    
    def getEntryList(budget):
        '''
        Receives a Budget object, and extracts the entries associated with it
        
        IN: Budget object
        OUT: List of Entry objects
        '''
        entryList = []
        for entryKey in budget.entryList:
            entryList += Entry.getEntry(entryKey)
        return entryList
    
    def getParticipantsAndPremissionsDict(budget):
        partAndPermDict = {}
        for entry in budget.participantsAndPermission:
            partAndPermDict.update(dict(json.loads(entry)))
        return partAndPermDict
            
            