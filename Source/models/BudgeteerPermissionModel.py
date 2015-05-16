from google.appengine.ext import ndb

class BudgeteerPermission(ndb.Model):
    permissionName = ndb.StringProperty()
    permissionLevel = ndb.IntegerProperty()