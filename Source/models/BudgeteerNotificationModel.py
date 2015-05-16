from google.appengine.ext import ndb

class BudgeteerNotification(ndb.Model):
    notifyIfAddedToBudget = ndb.BooleanProperty() #Invited to a budget
    notifyIfChangedEntry = ndb.BooleanProperty() #Remove\Add\Change entry




