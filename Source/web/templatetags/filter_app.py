from google.appengine.ext.webapp import template
register = template.create_template_register()
from models.BudgeteerModel import Budgeteer
from models.BudgetModel import Budget
@register.filter(name='getMyPermission')

def getMyPermission(budget,userName):
    budgeteerId = Budgeteer.getBudgeteerIdByUserName(userName)
    return Budget.getPermissionByBudgeteerId(budgeteerId,budget)
