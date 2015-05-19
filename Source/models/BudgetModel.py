from google.appengine.ext import ndb

class Budget(ndb.Model):
    tagsList = ndb.KeyProperty(kind='Tag',repeated=True) #list of tag id
    entryList = ndb.KeyProperty(kind='Entry',repeated=True) #list of entry id
    ownerId = ndb.KeyProperty() #user object stored key
    participantsAndPermission = ndb.StringProperty(repeated=True) #"liran123":5
    notifications = ndb.IntegerProperty()



