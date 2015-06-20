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
        temp_tagList = budget.tagList
        budget.tagList = []
        old_participants_id = Budget.getAssociatedBudgeteersId(budget)
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

        tag_name_list_before =[]
        for tag_key in temp_tagList:
            tag_name = Tag.getTagByKey(tag_key).description
            if tag_name and tag_name.lower() != "untagged":
                tag_name_list_before.append(Tag.getTagByKey(tag_key).description)

        for tag in tag_list.split(','):
            if not tag:
                break
            tag = tag.lower()
            if tag not in tag_name_list_before and tag != "untagged":
                tag_key = Tag.getTagKeyByName(tag)
                if not tag_key:
                    tag_object = Tag()
                    tag_object.description = tag
                    tag_object.count = 1
                    tag_object = tag_object.put()
                else:
                    tag_object = Tag.getTagByKey(tag_key)
                    tag_object.count += 1
                    tag_object = tag_object.put()
            else:
                continue
            tag_check=Tag.getTagByKey(tag_object)
            if tag_check.description.lower() != "untagged":
                budget.tagList.append(tag_object)

        for tag_key in temp_tagList:
            if not tag_key:
                break
            tag_name = Tag.getTagByKey(tag_key).description
            if tag_name.lower() == "untagged":
                continue
            if tag_name in tag_list.split(','):
                tag_key = Tag.getTagKeyByName(tag_name)
                budget.tagList.append(tag_key)
            else:
                tag_key = Tag.getTagKeyByName(tag_name)
                tag_object = Tag.getTagByKey(tag_key)
                if tag_object.count == 1:
                    Tag.removeTag(tag_object)
                else:
                    tag_object.count -= 1
                    tag_object.put()

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
            tag_object = Tag.getTagByKey(temp_entry.tagKey)
            if not tag_object:
                temp_entry.tagKey = Tag.getTagKeyByName("Untagged")
                Entry.updateEntry(temp_entry)

            else:
                tag_desc = tag_object.description
                if tag_desc not in tag_list.split(','):
                    temp_entry.tagKey = Tag.getTagKeyByName("Untagged")
                    Entry.updateEntry(temp_entry)

        Budget.addBudget(budget)

        src_budgeteer_key = Budgeteer.getBudgeteerById(long(budgeteer.key.id())).key
        src_username = Budgeteer.getBudgeteerById(long(budgeteer.key.id())).userName
        new_participants_id = Budget.getAssociatedBudgeteersId(budget)
        for participant_id in new_participants_id:
            if participant_id != budgeteer.key.id():
                budgeteer_participant = Budgeteer.get_by_id(participant_id)
                if participant_id in old_participants_id:
                    message_template = " Has Edited Budget {0}".format(budget.budgetName)
                    new_notification = BudgeteerNotification(srcBudgeteer=src_budgeteer_key,
                                                             dstBudgeteer=budgeteer_participant.key,
                                                             message=src_username + message_template,
                                                             link="/Budget/{0}".format(budget.key.id()),
                                                             read=False)
                    BudgeteerNotification.addNotification(new_notification)
                elif participant_id not in old_participants_id:
                    message_template = " Has Invited You To His Budget {0}".format(budget.budgetName)
                    new_notification = BudgeteerNotification(srcBudgeteer=src_budgeteer_key,
                                                             dstBudgeteer=budgeteer_participant.key,
                                                             message=src_username + message_template,
                                                             link="/Budget/{0}".format(budget.key.id()),
                                                             read=False)
                    BudgeteerNotification.addNotification(new_notification)
        for removed_participants_id in list(set(old_participants_id)-set(new_participants_id)):
            budgeteer_participant = Budgeteer.get_by_id(removed_participants_id)
            message_template = " Has Removed You From His Budget {0}".format(budget.budgetName)
            new_notification = BudgeteerNotification(srcBudgeteer=src_budgeteer_key,
                                                     dstBudgeteer=budgeteer_participant.key,
                                                     message=src_username + message_template,
                                                     link="/Budget/{0}".format(budget.key.id()),
                                                     read=False)
            BudgeteerNotification.addNotification(new_notification)

        self.response.write(json.dumps({'status':'OK'}))


app = webapp2.WSGIApplication([('/EditBudget/(.*)', EditBudgetHandler),
                               ('/SubmitEditedBudget/(.*)', SubmitEditedBudgetHandler)
                               ], debug=True)
