from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
from models.EntryModel import Entry
from models.TagModel import Tag
from models.BudgetModel import Budget
import json

class EditEntryHandler(webapp2.RequestHandler):
    def get(self, entryId):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
        else:
            self.redirect('/Login')
            return
        if not budgeteer:
            self.redirect('/Login')
            return

        entry = Entry.getEntryById(long(entryId))
        if entry.addedBy.id() != long(budgeteer.key.id()):
            self.redirect('/Budgets')
            return

        template_params = dict()
        budgetId = long(self.request.get('budgetId'))

        tagList = Budget.getTagList(Budget.getBudgetById(budgetId))
        tagNameList = []
        for tag in tagList:
            tagNameList += [tag.description]
        template.register_template_library('web.templatetags.filter_app')
        template_params['description'] = entry.description
        template_params['price'] = entry.amount
        template_params['tag'] = Tag.getTagByKey(entry.tagKey).description
        template_params['tagList'] = tagNameList
        template_params['budgetId'] = budgetId
        template_params['entryId'] = entryId
        html = template.render("web/templates/edit_entry.html", template_params)
        self.response.write(html)

class SubmitEditedEntryHandler(webapp2.RequestHandler):
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
        entryId = long(self.request.get('entryId'))
        # Fetch the entry
        entry = Entry.getEntryById(entryId)
        entry.description = description
        entry.tagKey = Tag.getTagKeyByName(tagname)
        entry.amount = float(price)

        entryKey = Entry.updateEntry(entry)
        print entryKey
        if not entryKey:
            self.error(403)
            self.response.write('Entry was not successfully submitted')
            return

        self.error(200)
        self.response.write(json.dumps({'status':'OK'}))
        return


app = webapp2.WSGIApplication([('/EditEntry/(.*)', EditEntryHandler),
                               ('/SubmitEditedEntry', SubmitEditedEntryHandler)], debug=True)
