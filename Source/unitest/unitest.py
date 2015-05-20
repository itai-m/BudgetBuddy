from google.appengine.ext import ndb
import json
from datetime import datetime

from BudgeteerModel import Budgeteer
from BudgeteerNotificationModel import BudgeteerNotification
from BudgetModel import Budget
from EntryModel import Entry
from TagModel import Tag


##Add Budgeteer at initial
rotem = Budgeteer(userName = "rotem1111",password="123123",firstName="Rotem",
                  lastName="ne",email="ro@ro.com",birthday=datetime.now(),
                  gender="f",budgeteerSettingNotifyIfAddedToBudget=True,budgeteerSettingNotifyIfChangedEntry=True,budgetsList =())
#Store bugeteer in datastore
rotem.put()
print "Added Budgeteer: " + rotem.firstName
#Add Budget


alist = []
alist.append(json.dumps({ "R0tem" : "Manager" })) #set permissionList

tgs = Tag(description="Salad")
tgs.put()
etry = Entry(description="hummos",amount=5.5,addedBy=rotem.key,creationDate=datetime.now(),tagId=tgs.key)

bgt = Budget(budgetName="BRBQ",creationDate=datetime.now(),tagsList=(),entryList=(),participantsAndPermission=alist)
Budget.addBudget(bgt)
Budget.addEntryToBudget(etry,bgt)

print "ok"
"""
for remove in Budget.query():
    remove.key.delete()
for remove in Budgeteer.query():
    remove.key.delete()
for remove in Entry.query():
    remove.key.delete()
for remove in Tag.query():
    remove.key.delete()
"""
