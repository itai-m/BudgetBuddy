from google.appengine.ext import ndb
from TagModel import Tag

class Budget(ndb.Model):
    tagsList = ndb.KeyProperty(kind='Tag',repeated=True) #list of tag id
    entryList = ndb.KeyProperty(kind='Entry',repeated=True) #list of entry id
    ownerId = ndb.KeyProperty() #user object stored key
    participantsAndPermission = ndb.StringProperty(repeated=True) #"liran123":5
    notifications = ndb.IntegerProperty()

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
        for tag in budget.tagsList:
            tagList += Tag.getTagDesc(tag)
        return tagList
        
