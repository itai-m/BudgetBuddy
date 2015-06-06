from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
from models.ChatMessageModel import ChatMessage
from models.BudgetModel import Budget
import datetime
import json

class SendChatMessageHandler(webapp2.RequestHandler):
    def post(self):
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

        chat_message = ChatMessage()
        chat_message.sent_by = budgeteer.key
        chat_message.budget_key = Budget.getBudgetById(long(self.request.get('budgetId'))).key
        chat_message.time = datetime.datetime.now()
        chat_message.text = self.request.get('message')
        ChatMessage.addChatMessage(chat_message)

        self.error(200)
        self.response.write(json.dumps({'status':'OK'}))
        return
app = webapp2.WSGIApplication([('/SendChatMessage', SendChatMessageHandler)], debug=True)
