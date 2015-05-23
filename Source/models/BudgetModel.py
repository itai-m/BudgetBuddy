from google.appengine.ext import ndb

import TagModel, EntryModel, BudgeteerModel
import json

'''
    Functionality tests:
        [X] Add Budget
        [X] Add Budget To Budgeteers
        [X] Get Budget By ID
        [X] Get Budget By Key
        [ ] Get Tag List
        [ ] Get Entry List
        [ ] Get Participants and Permission Dictionary
        [ ] Remove Budget
        [ ] Add Tag Key To Budget
        [ ] Remove Tag Key From Budget
        [ ] Add Entry To Budget
        [ ] Remove Entry To Budget
        [ ] Get Associated Budgeteers
        [ ] Remove Budgeteer From Participants and permission List
'''

class Budget(ndb.Model):
    budgetName = ndb.StringProperty()
    creationDate = ndb.DateProperty()
    tagList = ndb.KeyProperty(kind=TagModel.Tag, repeated=True)  # list of tag id
    entryList = ndb.KeyProperty(kind=EntryModel.Entry, repeated=True)  # list of limited available tags.
    participantsAndPermission = ndb.StringProperty(repeated=True)  # "liranObjectKey.id()":"Manager"

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
        participantsDict = Budget.getParticipantsAndPermissionsDict(budget)
        for budgeteerId in participantsDict.keys():
            budgeteer = BudgeteerModel.Budgeteer.getBudgeteerById(budgeteerId)
            BudgeteerModel.Budgeteer.addBudgetToBudgetList(budgeteer, budget)
        return budget.key.id()

    @staticmethod
    def getBudgetById(budgetId):
        '''
        Converts budget Id to budget.
        :param budgetId: id of the Budget object.
        :return: Budget object associated with the ID if exists, None if not.
        '''
        return Budget.get_by_id(budgetId)

    @staticmethod
    def getBudgetByKey(budgetKey):
        '''
        Converts budget key to budget.
        :param budgetKey: key of the Budget object.
        :return: Budget object associated with the key if exists, None if not.
        '''
        return budgetKey.get()

    @staticmethod
    def getTagList(budget):
        '''
        Receives a Budget object, and extracts the tags associated with it
        :param budget: Budget object
        :return: List of Tag objects
        '''
        tagList = []
        for tagKey in budget.tagList:
            tagList.append(TagModel.Tag.getTagByKey(tagKey))
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
            entryList.append(EntryModel.Entry.getEntryByKey(entryKey))
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
    def removeBudget(budget):
        '''
        Deletes a budget from the datastore.
        :param budget: Budget to delete.
        :return: None.
        '''
        # Delete all keys
        for entryKey in budget.entryList:
            EntryModel.Entry.removeEntry(entryKey)
        # Go through all the participants and remove the key from their list (?)
        participantIdList = Budget.getAssociatedBudgeteers(budget)
        for participantId in participantIdList:
            BudgeteerModel.Budgeteer.removeBudgetByKey(participantId, budget.key)
        # Remove budget from datastore
        budget.key.delete()

    @staticmethod
    def addTagKeyToBudget(tagKey,budget):
        '''
        :param tagKey: Tag key to add
        :param budget: Budget to add tag to
        :return: budget id.
        '''
        budget.tagList.append(tagKey)
        budget.put()
        return budget.key.id()

    @staticmethod
    def removeTagKeyFromBudget(tagKey, budget):
        '''
        :param tagKey: Tag key to remove
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
        entryKey = EntryModel.Entry.addEntryToDatastore(entry)
        budget.entryList.append(entryKey)
        budget.put()
        return entryKey.id()

    @staticmethod
    def RemoveEntryFromBudget(entryKey, budget):
        '''
        Receives an entry object, and removes it from input budget.
        :param entryKey: Entry object key to remove from the Budget.
        :param budget: Budget object to remove the entry from.
        :return: budget ID.
        '''
        budget.entryList.remove(entryKey)
        EntryModel.Entry.removeEntry(entryKey)
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

    @staticmethod
    def removeBudgeteerFromBudget(budgeteerId, budget):
        '''
        Receives a budget and budgeteerId in order to remove the budgeteerId from the participants and permission
        :param budgeteerId: Budgeteer id to remove from list
        :param budget: Budget object.
        :return: budget object id.
        '''
        participantsDict = Budget.getParticipantsAndPermissionsDict(budget)
        for budgeteerIdInList in participantsDict.keys():
            if budgeteerIdInList == budgeteerId:
                BudgeteerModel.Budgeteer.removeBudgetByKey(budgeteerId, budget.key)
                del participantsDict[budgeteerIdInList]  # removes from dictionary

        dictToStringList = []
        for dic in participantsDict:
            dictToStringList.append(json.dumps(dic))

        budget.participantsAndPermission = dictToStringList
        budget.put()
        return budget.key.id()
