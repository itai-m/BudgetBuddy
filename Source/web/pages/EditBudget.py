from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
from models.BudgetModel import Budget
from models.TagModel import Tag
from models.EntryModel import Entry
from models.BudgeteerNotificationModel import BudgeteerNotification
import datetime
import json

class EditBudgetHandler(webapp2.RequestHandler):
    def get(self,budget_id):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
        else:
            self.redirect('/Login')
            return
        if not budgeteer:
            self.redirect('/Login')
            return

        template.register_template_library('web.templatetags.filter_app')
        template_params = dict()
        tag_object_list = Tag.getAllTags()
        tag_name_pair_list = []

        budget=Budget.getBudgetById(long(budget_id))
        budgetBudgeteersId = Budget.getAssociatedBudgeteersId(budget)

        # Remove the "untagged" tag. the user should not be able to see it.
        temp_object_list = []
        for tag in tag_object_list:
            if tag.description != "Untagged":
                temp_object_list.append(tag)
        tag_object_list = temp_object_list

        if len(tag_object_list)%2 == 1:
            tag_object_list.append(None)
        for i in range (0,len(tag_object_list),2):
            if tag_object_list[i+1] == None:
                tag_name_pair_list.append([tag_object_list[i].description, None])
            else:
                tag_name_pair_list.append([tag_object_list[i].description, tag_object_list[i+1].description])

        temp_tag_list = Budget.getTagList(budget)
        budget_tag_list = []
        for tag in temp_tag_list:
            budget_tag_list.append(tag.description)
        template.register_template_library('web.templatetags.filter_app')
        template_params['userName'] = budgeteer.userName
        template_params['budget'] = budget
        template_params['budgetName'] = budget.budgetName
        template_params['tagnamePairList'] = tag_name_pair_list
        template_params['checkedTags'] = budget_tag_list
        template_params['budgetId'] = budget_id

        html = template.render("web/templates/edit_budget.html", template_params)
        self.response.write(html)


class SubmitEditedBudgetHandler(webapp2.RequestHandler):
    def get(self, budget_id):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
            if not budgeteer:
                self.redirect('/Login')
                return
        else:
            self.redirect('/Login')
            return
        budget_name = self.request.get('budgetName')
        tag_list = self.request.get('tagList')
        participant_list = self.request.get('participantList')

        budget = Budget.getBudgetById(long(budget_id))
        budget.budgetName = budget_name
        budget.creationDate = datetime.datetime.now()
        budget.tagList = []

        for participant in Budget.getAssociatedBudgeteersId(budget):
            Budget.removeBudgeteerFromBudget(participant, budget)

        # Add the Untagged entry to the budget.
        budget.participantsAndPermission = []

        untagged_key = Tag.getTagKeyByName("Untagged")
        if not untagged_key:
            untagged_key = Tag()
            untagged_key.description = "Untagged"
            untagged_key = Tag.addTagToDatastore(untagged_key)
        budget.tagList.append(untagged_key)

        for tag in tag_list.split(','):
            if not tag:
                break
            tag_key = Tag.getTagKeyByName(tag)
            if not tag_key:
                self.response.write('Unrecognized tag ' + tag)
                return
            budget.tagList.append(tag_key)

        for participant in participant_list.split(","):
            budgeteer_name = participant.split(":")[0]
            budgeteer_id = str(Budgeteer.getBudgeteerIdByUserName(budgeteer_name.lower()))
            if not budgeteer_id:
                self.response.write('No such username ' + budgeteer_name)
                return
            budgeteer_perm = participant.split(":")[1]
            if "Manager" != budgeteer_perm and "Partner" != budgeteer_perm and "Viewer" !=  budgeteer_perm:
                self.response.write('Unknown permission level ' + budgeteer_perm)
                return
            budget.participantsAndPermission.append(json.dumps({budgeteer_id : budgeteer_perm}))

        for entry in budget.entryList:
            temp_entry = Entry.getEntryByKey(entry)
            tag_desc = Tag.getTagByKey(temp_entry.tagKey)
            tag_desc = tag_desc.description
            if tag_desc not in tag_list.split(','):
                temp_entry.tagKey = Tag.getTagKeyByName("Untagged")
                Entry.updateEntry(temp_entry)

        message_template = " Has Invited You To His Budget {0}".format(budget.budgetName)
        src_budgeteer_key = Budgeteer.getBudgeteerById(long(budgeteer.key.id())).key
        src_username = Budgeteer.getBudgeteerById(long(budgeteer.key.id())).userName
        for participant_budgeteer_id in Budget.getAssociatedBudgeteersId(budget):
            if long(budgeteer.key.id()) != long(participant_budgeteer_id):
                dst_budgeteer_key = Budgeteer.getBudgeteerById(long(participant_budgeteer_id)).key
                new_notification = BudgeteerNotification(srcBudgeteer=src_budgeteer_key, dstBudgeteer=dst_budgeteer_key,
                                                         message=src_username + message_template,
                                                         link="/Budget/{0}".format(budget.key.id()),
                                                         read=False)
                BudgeteerNotification.addNotification(new_notification)

        Budget.addBudget(budget)
        self.response.write(json.dumps({'status':'OK'}))


app = webapp2.WSGIApplication([('/EditBudget/(.*)', EditBudgetHandler),
                               ('/SubmitEditedBudget/(.*)', SubmitEditedBudgetHandler)
                               ], debug=True)
