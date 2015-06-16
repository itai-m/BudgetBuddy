from google.appengine.ext.webapp import template
register = template.create_template_register()
from models.BudgeteerModel import Budgeteer
from models.BudgetModel import Budget
from models.EntryModel import Entry
from models.TagModel import Tag
from models.BudgeteerNotificationModel import BudgeteerNotification
import json
import calendar

@register.filter(name='budgeteer_key_to_username')
def budgeteer_key_to_username(budgeteer_key):
    return Budgeteer.getBudgeteerById(long(json.loads(budgeteer_key).keys()[0])).userName

@register.filter(name='get_notification_by_username')
def get_notification_by_username(user_name):
    notification_list = []
    budgeteer_id = Budgeteer.getBudgeteerIdByUserName(user_name)
    if budgeteer_id is None:
        return None
    budgeteer = Budgeteer.getBudgeteerById(budgeteer_id)
    if BudgeteerNotification.getNotificationsByDstKey(budgeteer.key):
        notification_list = BudgeteerNotification.getUnreadNotificationsByDstKey(budgeteer.key)
        return notification_list
    return None

@register.filter(name='getMyPermission')
def getMyPermission(budget, userName):
    budgeteerId = Budgeteer.getBudgeteerIdByUserName(userName)
    return Budget.getPermissionByBudgeteerId(budgeteerId, budget)

@register.filter(name='getMyPermissionById')
def getMyPermissionById(budget, dicIdAndPermission):
    return Budget.getPermissionByBudgeteerId(long(json.loads(dicIdAndPermission).keys()[0]), budget)


@register.filter(name='integer_to_month_name')
def integer_to_month_name(value):
    return calendar.month_name[value]

@register.filter(name='getEntryDescriptionByKey')
def getEntryDescriptionByKey(value):
    entry = Entry.getEntryByKey(value)
    return entry.description

@register.filter(name='getEntryAmountByKey')
def getEntryAmountByKey(value):
    entry = Entry.getEntryByKey(value)
    if entry.amount %1 == 0:
        return int(entry.amount)
    else:
        return entry.amount

@register.filter(name='getEntryTagDescriptionByKey')
def getEntryTagDescriptionByKey(value):
    entry = Entry.getEntryByKey(value)
    tg = Tag.getTagByKey(entry.tagKey)
    return tg.description

@register.filter(name='getUsernameByKey')
def getUsernameByKey(value):
    budgeteer = Budgeteer.getBudgeteerById(value.id())
    return budgeteer.userName

@register.filter(name='dateTimeToString')
def dateTimeToString(value):
    print value
    print "ASFSAOAKSFOASKF"
    return value.now().strftime("%Y-%m-%d %H:%M:%S")

@register.filter(name='getEntryAddedByByKey')
def getEntryAddedByByKey(value):
    entry = Entry.getEntryByKey(value)
    budgeteer = Budgeteer.getBudgeteerById(entry.addedBy.id())
    return budgeteer.userName

@register.filter(name='getEntryCreationDateByKey')
def getEntryCreationDateByKey(value):
    entry = Entry.getEntryByKey(value)
    return entry.creationDate

@register.filter(name='getTagPieDic')
def getTagPieDic(budget):
    tagPieDic={}
    tagList=Budget.getTagList(budget)

    for tag in tagList:
           tagName=tag.description
           tagAmountCount=getCountTagAmountInBudget(budget,tag.key)
           if(tagAmountCount>0):
               tagPieDic.update({str(tagName): (float(tagAmountCount)) })
    return tagPieDic


def getCountTagAmountInBudget(budget,tagKey):
    count=0.0
    for entryKey in budget.entryList:
        entry = Entry.getEntryByKey(entryKey)
        if(entry.tagKey==tagKey):
           count+=entry.amount
    return count


@register.filter(name='getUsersPieDic')
def getUsersPieDic(budget):

    usersPieDic={}
    budgeteerIdList=Budget.getAssociatedBudgeteersId(budget)

    for budgeteerId in budgeteerIdList:
           budgeteer=Budgeteer.getBudgeteerById(budgeteerId)
           budgeteerUserName=budgeteer.userName
           userAmountCount=getCountUserAmountInBudget(budget,budgeteer.key)
           if(userAmountCount>0):
               usersPieDic.update({str(budgeteerUserName): (float(userAmountCount)) })
    return usersPieDic


def getCountUserAmountInBudget(budget,budgeteerKey):
    count=0.0
    for entryKey in budget.entryList:
        entry = Entry.getEntryByKey(entryKey)
        if(entry.addedBy==budgeteerKey):
           count+=entry.amount
    return

@register.filter(name='username_to_image')
def username_to_image(user_name):
    budgeteer_id = Budgeteer.getBudgeteerIdByUserName(user_name)
    budgeteer = Budgeteer.getBudgeteerById(budgeteer_id)
    print budgeteer
    print budgeteer_id
    return  "../static/images/avatars/budgeteer" + str(budgeteer.avatar) + ".jpeg";
