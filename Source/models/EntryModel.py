from google.appengine.ext import ndb

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
    def updateEntry(updatedEntry):
        updatedEntry.put()
        return updatedEntry.key
    
    @staticmethod 
    def getEntryByKey(entryKey):
        return Entry.query(Entry.key == entryKey).get()
    
    @staticmethod
    def deleteEntry(entryKey):
        entryKey.delete()
        # TODO: Check if deletes all references to that object in the database




