import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

class Budgeteer(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    firstname = ndb.StringProperty()
    lastname = ndb.StringProperty()
    email = ndb.EmailProperty()
    birthday = ndb.DateProperty ()
    gender = ndb.StringProperty()
    notifications = ndb.IntegerProperty()
    budgets = ndb.ListProperty(Budget)
    

def registerNewUser(uname, pword, fname, lname, email, bday, gender, notifications, bugets):
    budgeteer = Budgeteer()
    budgeteer.username = uname
    budgeteer.password = pword
    budgeteer.firstname = fname
    budgeteer.lastname = lname
    budgeteer.email = email
    budgeteer.bday = birthday
    budgeteer.gender = gender
    budgeteer.notifications = notificatoins
    budgeteer.budgets = []
    ndb.put()
    
