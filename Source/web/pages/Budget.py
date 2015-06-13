from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
from models.BudgetModel import Budget
from models.EntryModel import Entry
import json
from models.ChatMessageModel import ChatMessage
class IndexHandler(webapp2.RequestHandler):
    def get(self, budgetId):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
            if not budgeteer:
                self.redirect('/Login')
                return
        else:
            self.redirect('/Login')
            return
        template.register_template_library('web.templatetags.filter_app')
        budget = Budget.getBudgetById(long(budgetId))
        template_params = dict()
        assoc_budgeteers = Budget.getAssociatedBudgeteersId(budget)
        for entry in budget.entryList:
            temp_entry = Entry.getEntryByKey(entry)
            print temp_entry
            budgeteer_id = long(Budgeteer.getBudgeteerByKey(temp_entry.addedBy).key.id())
            print budgeteer_id
            if  budgeteer_id not in assoc_budgeteers:
                Budget.removeEntriesByBudgeteerId(budget, budgeteer_id)

        template_params['chatMessages'] = ChatMessage.getChatMessagesByBudgetId((budgetId)).fetch()
        template_params['userName'] = budgeteer.userName
        template_params['userId'] = budgeteer.key.id()
        template_params['budget'] = Budget.getBudgetById(long(budgetId))
        template_params['budgetId'] = budgetId
        if  Budget.getPermissionByBudgeteerId(long(budgeteer.key.id()), budget) == "Manager":
            template_params['budgetManager'] = True
        else:
            template_params['budgetManager'] = False
        html = template.render("web/templates/budget.html", template_params)
        self.response.write(html)

class RemoveEntryHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
            if not budgeteer:
                self.redirect('/Login')
                return
        else:
            self.redirect('/Login')
            return

        entryId = long(self.request.get('entryId'))
        budgetId = long(self.request.get('budgetId'))

        budget = Budget.getBudgetById(budgetId)
        entry = Entry.get_by_id(entryId)
        my_permission = Budget.getPermissionByBudgeteerId(long(budgeteer.key.id()), budget)
        if my_permission != "Manager" and my_permission != "Partner":
            self.error(403)
            self.response.write("You have no permission to do so")
            return

        if not budget or not entry:
            self.error(403)
            self.response.write("There is no such entry")
            return

        Budget.RemoveEntryFromBudget(entry.key,budget)
        self.response.write(json.dumps({'status':'OK'}))

app = webapp2.WSGIApplication([
    ('/Budget/(.*)', IndexHandler),
    ('/RemoveEntryFromBudget', RemoveEntryHandler)
], debug=True)
