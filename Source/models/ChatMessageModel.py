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
        return message.put()


