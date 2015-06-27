from google.appengine.ext import ndb
from models.BudgetModel import Budget

class ChatMessage(ndb.Model):
    text = ndb.StringProperty()
    sent_by = ndb.KeyProperty()
    budget_key = ndb.KeyProperty()
    time = ndb.DateTimeProperty()

    @staticmethod
    def getChatMessagesByBudgetId(budget_id):
        '''
        This function receives a budget key and returns a list of all chat messages belong to that budget.
        :param budget_key: Budget id.
        :return: a list of chat messages object.
        '''
        return ChatMessage.query(ChatMessage.budget_key == Budget.getBudgetById(long(budget_id)).key).order(-ChatMessage.time)


    @staticmethod
    def addChatMessage(message):
        '''
        Receives a message object, return the object key after submission to database.
        :param message: ChatMessage object..
        :return: the key after enter to datastore.
        '''
        message.put()
        return message.key


    @staticmethod
    def clearChatMessagesForBudgetId(budget_id):
        '''
        Clean all messages associated with a budget id.
        :param message: budget id.
        :return: None
        '''
        msg_list = ChatMessage.query(ChatMessage.budget_key == Budget.getBudgetById(long(budget_id)).key).fetch()
        for msg in msg_list:
            msg.key.delete()
        return None