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
    def getEntry(entryKey):
        return Entry.query(Entry.key == entryKey)





