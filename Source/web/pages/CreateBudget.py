from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
from models.BudgetModel import Budget
from models.EntryModel import Entry
from models.TagModel import Tag
import json
import datetime

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

        template_params = dict()
        tagObjectList = Tag.getAllTags()
        tagnamePairList = []

        if len(tagObjectList)%2 == 1:
            tagObjectList.append(None)
        for i in range (0,len(tagObjectList),2):
            if tagObjectList[i+1] == None:
                tagnamePairList.append([tagObjectList[i].description, None])
            else:
                tagnamePairList.append([tagObjectList[i].description, tagObjectList[i+1].description])

        template_params['tagnamePairList'] = tagnamePairList
        template_params['userName'] = budgeteer.userName
        html = template.render("web/templates/CreateBudget.html", template_params)
        self.response.write(html)


class CreateChecksHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
            if not budgeteer:
                self.redirect('/Login')
                return
        else:
            self.redirect('/Login')
            return
        username = self.request.get('username')
        if not Budgeteer.budgeteerUserNameExist(username):
            self.response.write('No such username.')
            return
        self.response.write(json.dumps({'status':'OK'}))

class SubmitNewBudgetHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
            if not budgeteer:
                self.redirect('/Login')
                return
        else:
            self.redirect('/Login')
            return
        budgetName = self.request.get('budgetName')
        tagList = self.request.get('tagList')
        participantList = self.request.get('participantList')

        budget = Budget()
        budget.budgetName = budgetName
        budget.creationDate = datetime.datetime.now()
        budget.entryList = []
        budget.tagList = []
        budget.participantsAndPermission = []

        for tag in tagList.split(','):
            tag_key = Tag.getTagKeyByName(tag)
            if not tag_key:
                self.response.write('Unrecognized tag ' + tag)
                return
            budget.tagList.append(tag_key)
        for participant in participantList.split(","):
            budgeteer_name = participant.split(":")[0]
            budgeteer_id = str(Budgeteer.getBudgeteerIdByUserName(budgeteer_name.lower()))
            if not budgeteer_id:
                self.response.write('No such username ' + budgeteer_name)
                return
            budgeteer_perm = participant.split(":")[1]
            print budgeteer_perm
            if "Manager" != budgeteer_perm and "Partner" != budgeteer_perm and "Viewer" !=  budgeteer_perm:
                self.response.write('Unknown permission level ' + budgeteer_perm)
                return
            budget.participantsAndPermission.append(json.dumps({budgeteer_id : budgeteer_perm}))
        Budget.addBudget(budget)
        self.response.write(json.dumps({'status':'OK'}))



app = webapp2.WSGIApplication([('/CreateBudget', IndexHandler),
                               ('/CreateCheck',CreateChecksHandler),
                               ('/SubmitNewBudget',SubmitNewBudgetHandler)],
                              debug=True)
