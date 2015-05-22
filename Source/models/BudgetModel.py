from google.appengine.ext import ndb
from TagModel import Tag
from EntryModel import Entry
from BudgeteerModel import Budgeteer
import json

class Budget(ndb.Model):
    budgetName = ndb.StringProperty()
    creationDate = ndb.DateProperty()
    tagList = ndb.KeyProperty(kind=Tag,repeated=True) #list of tag id
    entryList = ndb.KeyProperty(kind=Entry,repeated=True) #list of limited available tags. decided by manager
    participantsAndPermission = ndb.StringProperty(repeated=True) # "liranObjectKey":"Manager"


    @staticmethod
    def addBudget(budget):
        '''
        Receives a Budget, and adds it to the datastore, and also to all the associated budgeteers
        :param budget: Budget object
        :return: Budget object id after submission.
        '''
        budget.put()
        Budget.addBudgetToBudgeteers(budget)
        return budget.key.id()

    @staticmethod
    def addBudgetToBudgeteers(budget):
        '''
        Receives a budget, and add the budget id to all the budgeteers in the participants list.
        :param budget: Budget object.
        :return: budget object id.
        '''
        participantsDict=Budget.getParticipantsAndPermissionsDict(budget)
        for budgeteerId in participantsDict.keys():
            budgeteer = Budgeteer.getBudgeteerById(budgeteerId)
            Budgeteer.addBudgetToBudgetList(budgeteer, budget)

    @staticmethod
    def getBudgetByID(budgetId):
        '''
        Converts budget Id to budget.
        :param budgetId: id of the Budget object.
        :return: Budget object associated with the ID if exists, None if not.
        '''
        return Budget.query(Budget.key.id() == budgetId).get()

    def getTagList(budget):
        '''
        Receives a Budget object, and extracts the tags associated with it
        :param budget: Budget object
        :return: List of Tag objects
        '''
        tagList = []
        for tagKey in budget.tagList:
            tagList.append(Tag.getTagByKey(tagKey))
        return tagList

    @staticmethod
    def getEntryList(budget):
        '''
        Receives a Budget object, and extracts the entries associated with it
        :param budget: Budget object
        :return: List of Entry objects
        '''
        entryList = []
        for entryKey in budget.entryList:
            entryList.append(Entry.getEntryByKey(entryKey))
        return entryList

    @staticmethod
    def getParticipantsAndPermissionsDict(budget):
        '''
        Gets a budget object, and converts the participantsAndPermission to dictionary
        of [Key]=Value pairs as: [ParticipantID]=PermissionLevel
        :param budget:
        :return: Dictionary of [ParticipantID]=PermissionLevel
        '''
        partAndPermDict = {}
        for entry in budget.participantsAndPermission:
            partAndPermDict.update(dict(json.loads(entry)))
        return partAndPermDict

    @staticmethod
    def deleteBudget(budget):
        '''
        Deletes a budget from the datastore.
        :param budget: Budget to delete.
        :return: None.
        '''
        # Delete all keys
        for entryKey in budget.entryList:
            Entry.deleteEntry(entryKey)
        # Go through all the participants and remove the key from their list (?)
        participantIdList = Budget.getAssociatedBudgeteers(budget)
        for participantId in participantIdList:
            Budgeteer.removeBudgetByKey(participantId, budget.key)
        # Remove budget from datastore
        budget.key.delete()

    @staticmethod
    def addTagToBudget(tagKey,budget):
        '''
        :param tag: Tag to add
        :param budget: Budget to add tag to
        :return: budget id.
        '''
        budget.tagList.append(tagKey)
        budget.put()
        return budget.key.id()

    @staticmethod
    def removeTagFromBudget(tagKey, budget):
        '''
        :param tag: Tag to remove
        :param budget: Budget to remove tag from
        :return: budget id.
        '''
        budget.tagList.remove(tagKey)
        budget.put()
        return budget.key.id()

    @staticmethod
    def addEntryToBudget(entry,budget):
        '''
        Receives an entry object, and adds it to the input budget.
        :param entry: Entry object to add to the Budget.
        :param budget: Budget object to insert the Entry into.
        :return: Entry ID.
        '''
        entryKey = Entry.addEntry(entry)
        budget.entryList.append(entryKey)
        budget.put()
        return entryKey.id()

    @staticmethod
    def RemoveEntryFromBudget(entry, budget):
        '''
        Receives an entry object, and removes it from input budget.
        :param entry: Entry object to remove from the Budget.
        :param budget: Budget object to remove the entry from.
        :return: budget ID.
        '''
        budget.entryList.remove(entry.key)
        Entry.deleteEntry(entry.key)
        budget.put()
        return budget.key.id()

    @staticmethod
    def getAssociatedBudgeteers(budget):
        '''
        Receives a budget and returns a list of the budgeteer ids associated with that budget.
        :param budget: Budget object
        :return: List of budgeteer ids associated with the buddget.
        '''
        participantIdList = []
        dict = Budget.getParticipantsAndPermissionsDict(budget)
        for participantId in dict.keys():
            participantIdList.append(participantId)
        return participantIdList