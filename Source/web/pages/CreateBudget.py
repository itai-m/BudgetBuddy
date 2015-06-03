from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
from models.BudgetModel import Budget
from models.EntryModel import Entry
from models.TagModel import Tag

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

app = webapp2.WSGIApplication([('/CreateBudget', IndexHandler)], debug=True)
