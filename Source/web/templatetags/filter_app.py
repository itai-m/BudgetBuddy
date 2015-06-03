from google.appengine.ext.webapp import template
register = template.create_template_register()
from models.BudgeteerModel import Budgeteer
from models.BudgetModel import Budget
from models.EntryModel import Entry
from models.TagModel import Tag

import calendar

@register.filter(name='getMyPermission')
def getMyPermission(budget, userName):
    budgeteerId = Budgeteer.getBudgeteerIdByUserName(userName)
    return Budget.getPermissionByBudgeteerId(budgeteerId, budget)

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
    return entry.amount

@register.filter(name='getEntryTagDescriptionByKey')
def getEntryTagDescriptionByKey(value):
    entry = Entry.getEntryByKey(value)
    tg = Tag.getTagByKey(entry.tagKey)
    return tg.description

@register.filter(name='getEntryAddedByByKey')
def getEntryAddedByByKey(value):
    entry = Entry.getEntryByKey(value)
    budgeteer = Budgeteer.getBudgeteerById(entry.addedBy.id())
    return budgeteer.userName

@register.filter(name='getEntryCreationDateByKey')
def getEntryCreationDateByKey(value):
    entry = Entry.getEntryByKey(value)
    return entry.creationDate

