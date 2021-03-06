from google.appengine.ext.webapp import template
import webapp2
from models.BudgeteerModel import Budgeteer
from models.ChatMessageModel import ChatMessage
from models.BudgetModel import Budget
import datetime
import json
import time


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
        budget = Budget.getBudgetById(long(self.request.get('budgetId')))
        budget_key = Budget.getBudgetById(long(self.request.get('budgetId'))).key


        permission = Budget.getPermissionByBudgeteerId(budgeteerId, budget)
        if not budget.chatEnabled and permission != "Manager" and  self.request.get('message'):
            self.error(403)
            self.response.write('Announcement box is disabled.')
            return

        # If message is not set, return the current message for this budget.
        if self.request.get('message'):
            chat_message = ChatMessage()
            chat_message.sent_by = budgeteer.key
            chat_message.budget_key = budget_key
            chat_message.time = datetime.datetime.now()
            chat_message.text = self.request.get('message')
            ChatMessage.addChatMessage(chat_message)

        list_to_write = []
        for chat in  ChatMessage.getChatMessagesByBudgetId(budget_key.id()).fetch():
            list_to_write.append({"time":chat.time.strftime("%Y-%m-%d %H:%m"),"username":Budgeteer.getBudgeteerById(chat.sent_by.id()).userName,"text":chat.text.encode("utf-8","ignore")})
        self.error(200)
        self.response.write(json.dumps(
            {
                'list':list_to_write,
                'status':'OK'
            }
        ))

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
            self.response.write('Only budget manager can clean Announcement box.')
            return
        ChatMessage.clearChatMessagesForBudgetId(budgetId)
        self.error(200)
        self.response.write(json.dumps({'status':'OK'}))
        return

class ToggleChatHandler(webapp2.RequestHandler):
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
        chatStatus = self.request.get('chatStatus')

        permission = Budget.getPermissionByBudgeteerId(budgeteerId, Budget.getBudgetById(budgetId))
        if permission != "Manager":
            self.error(403)
            self.response.write('Only budget manager toggle chat.')
            return
        Budget.setChatEnabledDisabledByBudgetId(budgetId, chatStatus)
        self.error(200)
        self.response.write(json.dumps({'status':'OK'}))
        return

app = webapp2.WSGIApplication([('/SendChatMessage', SendChatMessageHandler),
                               ('/ClearChatMessages', ClearChatMessagesHandler),
                               ('/ToggleChat', ToggleChatHandler)
                               ], debug=True)
