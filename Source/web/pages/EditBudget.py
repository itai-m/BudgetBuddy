from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
from models.BudgetModel import Budget
from models.TagModel import Tag

class EditBudgetHandler(webapp2.RequestHandler):
    def get(self,budgetId):
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
        tagObjectList = Tag.getAllTags()
        tagnamePairList = []

        budget=Budget.getBudgetById(long(budgetId))
        budgetBudgeteersId = Budget.getAssociatedBudgeteersId(budget)


        if len(tagObjectList)%2 == 1:
            tagObjectList.append(None)
        for i in range (0,len(tagObjectList),2):
            if tagObjectList[i+1] == None:
                tagnamePairList.append([tagObjectList[i].description, None])
            else:
                tagnamePairList.append([tagObjectList[i].description, tagObjectList[i+1].description])

        template_params['userName'] = budgeteer.userName
        template_params['budget'] = budget
        template_params['budgetName'] = budget.budgetName
        template_params['tagnamePairList'] = tagnamePairList


        html = template.render("web/templates/EditBudget.html", template_params)
        self.response.write(html)

app = webapp2.WSGIApplication([('/EditBudget/(.*)', EditBudgetHandler)], debug=True)
