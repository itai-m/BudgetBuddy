from google.appengine.ext import ndb

class Entry(ndb.Model):
    description = ndb.StringProperty()
    amount = ndb.FloatProperty()
    ownerId = ndb.KeyProperty()
    creationDate = ndb.DateProperty()
    tagId = ndb.KeyProperty()


    @staticmethod 
    def getEntry(entryKey):
        return Entry.query(Entry.key == entryKey)
    
    @staticmethod
    def deleteEntry(entryKey):
        entryKey.delete()
        # TODO: Check if deletes all references to that object in the database
        





