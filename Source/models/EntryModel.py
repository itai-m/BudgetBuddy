from google.appengine.ext import ndb

class Entry(ndb.Model):
    description = ndb.StringProperty()
    amount = ndb.FloatProperty()
    ownerId = ndb.KeyProperty()
    creationDate = ndb.DateProperty()
    tagId = ndb.KeyProperty()




