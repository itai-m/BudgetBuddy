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
        budget_key = Budget.getBudgetById(long(self.request.get('budgetId'))).key
        chat_message = ChatMessage()
        chat_message.sent_by = budgeteer.key
        chat_message.budget_key = budget_key
        chat_message.time = datetime.datetime.now()
        chat_message.text = self.request.get('message')

        ChatMessage.addChatMessage(chat_message)
        list_to_write = []
        for chat in  ChatMessage.getChatMessagesByBudgetId(budget_key.id()).fetch():
            list_to_write.append({"time":chat.time.strftime("%Y-%m-%d %H:%m"),"username":Budgeteer.getBudgeteerById(chat.sent_by.id()).userName,"text":chat.text})
        self.error(200)
        self.response.write(json.dumps(
            {
                'time':str(chat_message.time.strftime("%Y-%m-%d %H:%m")),
                'username':str(budgeteer.userName),
                'text':str(chat_message.text),
                'list':list_to_write,
                'status':'OK'
            }
        ))
        return

class ClearChatMessagesHandler(webapp2.RequestHandler):
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
        budgetId = long(self.request.get('budgetId'))

        permission = Budget.getPermissionByBudgeteerId(budgeteerId, Budget.getBudgetById(budgetId))
        if permission != "Manager":
            self.error(403)
            self.response.write('Only budget manager can clean chat.')
            return
        ChatMessage.clearChatMessagesForBudgetId(budgetId)
        self.error(200)
        self.response.write(json.dumps({'status':'OK'}))
        return

app = webapp2.WSGIApplication([('/SendChatMessage', SendChatMessageHandler),
                               ('/ClearChatMessages', ClearChatMessagesHandler)
                               ], debug=True)
