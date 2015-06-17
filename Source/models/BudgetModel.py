from google.appengine.ext import ndb
import TagModel
import EntryModel
import BudgeteerModel
import json


'''
    Functionality tests:
        [X] Add Budget
        [X] Add Budget To Budgeteers
        [X] Get Budget By ID
        [X] Get Budget By Key
        [X] Get Participants and Permission Dictionary
        [X] Get Associated Budgeteers
        [X] Get Permission By Budgeteer ID
        [X] Remove Budgeteer From Participants and permission List
        [X] Remove Budget
        [X] Add Tag Key To Budget
        [X] Get Tag List
        [X] Remove Tag Key From Budget
        [X] Add Entry To Budget
        [X] Get Entry List
        [X] Remove Entry To Budget
'''

class Budget(ndb.Model):
    budgetName = ndb.StringProperty()
    creationDate = ndb.DateProperty()
    tagList = ndb.KeyProperty(kind=TagModel.Tag, repeated=True)  # list of tag id
    entryList = ndb.KeyProperty(kind=EntryModel.Entry, repeated=True)  # list of limited available tags.
    participantsAndPermission = ndb.StringProperty(repeated=True)  # " "liranObjectKey.id()":"Manager" "
    chatEnabled = ndb.BooleanProperty();

    @staticmethod
    def addBudget(budget):
        '''
        Receives a Budget, and adds it to the data store, and also to all the associated budgeteers
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
        participantsDictList = Budget.getAssociatedBudgeteersId(budget)
        for participant in participantsDictList:
            budgeteer = BudgeteerModel.Budgeteer.getBudgeteerById(participant)
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
        listOfDict = {}
        for entry in budget.participantsAndPermission:
            listOfDict.update(dict(json.loads(entry)))
        return listOfDict

    @staticmethod
    def removeBudget(budget):
        '''
        Deletes a budget from the data store.
        :param budget: Budget to delete.
        :return: None.
        '''
        # Delete all keys
        for entryKey in budget.entryList:
            EntryModel.Entry.removeEntry(entryKey)
        # Go through all the participants and remove the key from their list (?)
        participantIdList = Budget.getAssociatedBudgeteersId(budget)
        for participantId in participantIdList:
            BudgeteerModel.Budgeteer.removeBudgetByKey(participantId, budget.key)
        for tag_key in budget.tagList:
            tag_object=TagModel.Tag.getTagByKey(tag_key)
            if tag_object.count == 1:
               TagModel.Tag.removeTag(tag_object)
            else:
                tag_object.count -= 1
                tag_object.put()


        # Remove budget from data store
        budget.key.delete()

    @staticmethod
    def addTagKeyToBudget(tagKey, budget):
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
    def addEntryToBudget(entry, budget):
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
    def getAssociatedBudgeteersId(budget):
        '''
        Receives a budget and returns a list of the budgeteer ids associated with that budget.
        :param budget: Budget object
        :return: List of budgeteer ids associated with the budget.
        '''
        participantIdList = []
        participantsDictList = Budget.getParticipantsAndPermissionsDict(budget)
        for participantId in participantsDictList.keys():
            participantIdList.append(long(participantId))
        return participantIdList

    @staticmethod
    def getPermissionByBudgeteerId(budgeteerId, budget):
        '''
        Gets a budgeteer Id and converts its permission on a specified budget
        :param budgeteerId: budgeteer Id stored in the budget list
        :param budget: the budget itself
        :return: permission string if exists, None if not in list
        '''
        permList = Budget.getParticipantsAndPermissionsDict(budget)
        return permList[str(budgeteerId)]

    @staticmethod
    def removeBudgeteerFromBudget(budgeteerId, budget):
        '''
        Receives a budget and budgeteerId in order to remove the budgeteerId from the participants and permission
        :param budgeteerId: Budgeteer id to remove from list
        :param budget: Budget object.
        :return: budget object id.
        '''
        participants_dict = Budget.getParticipantsAndPermissionsDict(budget)
        for budgeteerIdInDict in participants_dict.keys():
            if str(budgeteerId) == budgeteerIdInDict:
                BudgeteerModel.Budgeteer.removeBudgetByKey(budgeteerId, budget.key)
                del participants_dict[budgeteerIdInDict]

        dict_to_string_list = []
        for key, value in participants_dict.items():
            dict_to_string_list.append(json.dumps({key: value}))
        budget.participantsAndPermission = dict_to_string_list
        budget.put()
        return budget.key.id()

    @staticmethod
    def hasAddEditEntryPermissions(budgeteerId, budgetId):
        '''
        Receives a budgetId and budgeteerId and returns whether that budgeteer has editing/adding permissions
        :param budgeteerId: Budgeteer id to verify adding permission - Should be a Integer/Long
        :param budgetId: Budget id to check Add / Edit permissions for said budgeteer. - Should be Integer/Long
        :return: true if editing/adding permissions are present, false otherwise.
        '''
        myPermission = Budget.getPermissionByBudgeteerId(budgeteerId,Budget.getBudgetById(budgetId))
        return myPermission == "Manager" or myPermission == "Partner"

    @staticmethod
    def removeEntriesByBudgeteerId(budget, budgeteerId):
        for entry in budget.entryList:
            temp_entry = EntryModel.Entry.getEntryByKey(entry)
            if BudgeteerModel.Budgeteer.getBudgeteerById(budgeteerId).key == temp_entry.addedBy:
                Budget.RemoveEntryFromBudget(entry, budget)
                EntryModel.Entry.removeEntry(entry)

    @staticmethod
    def setChatEnabledDisabledByBudgetId(budgetId, chatEnabled):
        if chatEnabled == "true":
            chatEnabled = True
        else:
            chatEnabled = False
        budget = Budget.getBudgetById(budgetId)
        budget.chatEnabled = chatEnabled
        budget.put()
