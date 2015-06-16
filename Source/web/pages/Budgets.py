from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
from models.BudgetModel import Budget
from models.BudgeteerNotificationModel import BudgeteerNotification
import json


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
            if not budgeteer:
                self.redirect('/Login')
                return
        else:
            self.redirect('/Login')
            return

        reverse_order = True

        template.register_template_library('web.templatetags.filter_app')
        template_params = dict()
        if self.request.get('sort_by'):
            sort_by = self.request.get('sort_by')
            if self.request.get('reverse_order'):
                reverse_order = self.request.get('reverse_order')
                if reverse_order == "False":
                    reverse_order = False
                else:
                    reverse_order = True
                template_params['budgetList'] = Budgeteer.getBudgetList(budgeteer, sort_by = sort_by, reverse = reverse_order)
            else:
                template_params['budgetList'] = Budgeteer.getBudgetList(budgeteer, sort_by = sort_by)
        else:
            template_params['budgetList'] = Budgeteer.getBudgetList(budgeteer)

        template_params['reverse'] = not reverse_order
        template_params['userName'] = budgeteer.userName
        html = template.render("web/templates/budgets.html", template_params)
        self.response.write(html)

class RemoveBudgetHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
            if not budgeteer:
                self.redirect('/Login')
                return
        else:
            self.redirect('/Login')
            return
        budgetId = long(self.request.get('budgetId'))
        budget = Budget.getBudgetById(budgetId)

        if budget is None:
            self.error(404)
            self.response.write("There is no such budget")
            return

        my_permission = Budget.getPermissionByBudgeteerId(long(budgeteer.key.id()), budget)

        if my_permission is None or my_permission != "Manager":
            self.error(403)
            self.response.write("You have no permission to do so")
            return

        Budget.removeBudget(budget)
        self.response.write(json.dumps({'status':'OK'}))

class ExitBudgetHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
            if not budgeteer:
                self.redirect('/Login')
                return
        else:
            self.redirect('/Login')
            return

        budgetId = long(self.request.get('budgetId'))
        budget = Budget.getBudgetById(budgetId)

        if budget is None:
            self.error(404)
            self.response.write("There is no such budget")
            return

        my_permission = Budget.getPermissionByBudgeteerId(long(budgeteer.key.id()), budget)

        if my_permission is None:
            self.error(403)
            self.response.write("You have no permission to do so")
            return

        if my_permission == "Manager":
            self.error(404)
            self.response.write("You can't quit your budget, you have remove it")
            return

        message_template = " Has Exited From Budget {0}".format(budget.budgetName)
        src_budgeteer_key = Budgeteer.getBudgeteerById(long(budgeteer.key.id())).key
        src_username = Budgeteer.getBudgeteerById(long(budgeteer.key.id())).userName
        for participant_budgeteer_id in Budget.getAssociatedBudgeteersId(budget):
            if long(budgeteer.key.id()) != long(participant_budgeteer_id):
                dst_budgeteer_key = Budgeteer.getBudgeteerById(long(participant_budgeteer_id)).key
                new_notification = BudgeteerNotification(srcBudgeteer=src_budgeteer_key, dstBudgeteer=dst_budgeteer_key,
                                                         message=src_username + message_template,
                                                         link="/Budget/{0}".format(budgetId))
                BudgeteerNotification.addNotification(new_notification)

        Budget.removeBudgeteerFromBudget(long(budgeteer.key.id()), budget)
        self.response.write(json.dumps({'status':'OK'}))


app = webapp2.WSGIApplication([
    ('/Budgets', IndexHandler),
    ('/RemoveBudgetFromBudget', RemoveBudgetHandler),
    ('/ExitBudget', ExitBudgetHandler)
], debug=True)
