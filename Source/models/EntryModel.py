from google.appengine.ext import ndb

class Entry(ndb.Model):
    description = ndb.StringProperty()
    amount = ndb.FloatProperty()
    addedBy = ndb.KeyProperty()
    creationDate = ndb.DateProperty()
    tagId = ndb.KeyProperty()

    @staticmethod
    def addEntryToDatastore(entry):
        '''
        Receives an entry object, and adds it to the Datastore.
        :param entry: Entry object to be added.
        :return: Entry key after the submission to datastore.
        '''
        entry.put()
        return entry.key

    @staticmethod
    def updateEntry(updatedEntry):
        '''
        updates an entry object.
        :param updatedEntry: Entry object.
        :return: id of the entry object.
        '''
        updatedEntry.put()
        return updatedEntry.key.id()
    
    @staticmethod 
    def getEntryByKey(entryKey):
        '''
        Receives an entry key, and returns the entry object.
        :param entryKey: entry key.
        :return: Entry object.
        '''
        return entryKey.get()
    
    @staticmethod
    def removeEntry(entryKey):
        '''
        Removes an Entry from the Datastore.
        :param entryKey: key of the Entry obejct to remove.
        :return: returns None
        '''
        entryKey.delete()
        return None






