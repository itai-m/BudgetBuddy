from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
from models.BudgetModel import Budget

class AddEntryHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.cookies.get('budgeteerIdToken'):
            budgeteer = Budgeteer.getBudgeteerById(long(self.request.cookies.get('budgeteerIdToken')))
            if not budgeteer:
                self.redirect('/Login')
                return
        else:
            self.redirect('/Login')
            return
        '''
        if not self.request.cookies.get('budgetId'):
            self.redirect('/Budgets')
            return  
        budgetId = self.request.cookies.get('budgetId')
        '''
        budgetId = 5207287069147136
        # Prepare a list of tag names.
        tagList = Budget.getTagList(Budget.getBudgetById(budgetId))
        tagNameList = []
        for tag in tagList:
            tagNameList += [tag.description]
        
        template_params = dict()
        template_params['tagList'] = tagNameList
        template_params['userName'] = budgeteer.userName
        html = template.render("web/templates/add_entry.html", template_params)
        self.response.write(html)

app = webapp2.WSGIApplication([('/AddEntry', AddEntryHandler)], debug=True)
