from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
from models.BudgetModel import Budget
from models.EntryModel import Entry
from models.TagModel import Tag
from models.BudgeteerNotificationModel import BudgeteerNotification
import json

import datetime
class AddEntryHandler(webapp2.RequestHandler):
    def get(self, budgetId):
        budgeteerId = None
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteerId = long(self.request.cookies.get('budgeteerIdToken'))
            budgeteer = Budgeteer.getBudgeteerById(budgeteerId)
            if not budgeteer:
                self.redirect('/Login')
                return
        else:
            self.redirect('/Login')
            return

        if not budgetId:
            self.redirect('/Budgets')
            return
        budgetId = long(budgetId)
        # Verify that the user has sufficient permissions
        if not Budget.hasAddEditEntryPermissions(budgeteerId, budgetId):
            self.redirect('/Budgets')
            return

        # Prepare a list of tag names.
        tagList = Budget.getTagList(Budget.getBudgetById(budgetId))
        tagNameList = []
        for tag in tagList:
            tagNameList += [tag.description]
        template.register_template_library('web.templatetags.filter_app')
        template_params = dict()
        template_params['budgetId'] = budgetId
        template_params['tagList'] = tagNameList
        template_params['userName'] = budgeteer.userName
        html = template.render("web/templates/add_entry.html", template_params)
        self.response.write(html)

class SubmitEntryHandler(webapp2.RequestHandler):
    def get(self):
        budgeteerId = None
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteerId = long(self.request.cookies.get('budgeteerIdToken'))
            budgeteer = Budgeteer.getBudgeteerById(budgeteerId)
            if not budgeteer:
                self.redirect('/Login')
                return
        else:
            self.redirect('/Login')
            return

        budgetId = long(self.request.get('budgetId'))
        # Verify that the user has sufficient permissions
        if not Budget.hasAddEditEntryPermissions(budgeteerId, budgetId):
            self.redirect('/Budgets')
            return
        # Prepare a list of tag names.
        description = self.request.get('description')
        price = self.request.get('price')
        tagname = self.request.get('tagname')

        # Create the entry
        entry = Entry()
        entry.description = description
        entry.tagKey = Tag.getTagKeyByName(tagname)
        entry.addedBy = budgeteer.key
        entry.creationDate = datetime.datetime.now()
        entry.amount = float(price)

        budget = Budget.getBudgetById(budgetId)

        message_template = " Has Added a New Entry In {0}".format(budget.budgetName)
        src_budgeteer_key = Budgeteer.getBudgeteerById(long(budgeteerId)).key
        src_username = Budgeteer.getBudgeteerById(long(budgeteerId)).userName
        for participant_budgeteer_id in Budget.getAssociatedBudgeteersId(budget):
            if long(budgeteerId) != long(participant_budgeteer_id):
                dst_budgeteer_key = Budgeteer.getBudgeteerById(long(participant_budgeteer_id)).key

                new_notification = BudgeteerNotification(srcBudgeteer=src_budgeteer_key, dstBudgeteer=dst_budgeteer_key,
                                                         message=src_username + message_template,
                                                         link="/Budget/{0}".format(budgetId),
                                                         read=False)
                BudgeteerNotification.addNotification(new_notification)

        entryKey = Budget.addEntryToBudget(entry, Budget.getBudgetById(long(budgetId)))
        if not entryKey:
            self.error(403)
            self.response.write('Entry was not successfully submitted')
            return

        self.error(200)
        self.response.write(json.dumps({'status':'OK'}))
        return

app = webapp2.WSGIApplication([('/AddEntry/(.*)', AddEntryHandler),
                               ('/SubmitEntry', SubmitEntryHandler)],
                              debug=True)
