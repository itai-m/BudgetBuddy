from google.appengine.ext.webapp import template
register = template.create_template_register()
from models.BudgeteerModel import Budgeteer
from models.BudgetModel import Budget

import calendar

@register.filter(name='getMyPermission')
def getMyPermission(budget, userName):
    budgeteerId = Budgeteer.getBudgeteerIdByUserName(userName)
    return Budget.getPermissionByBudgeteerId(budgeteerId, budget)

@register.filter(name='integer_to_month_name')
def integer_to_month_name(value):
    return calendar.month_name[value]

