from google.appengine.ext import ndb
import hashlib
from datetime import datetime
import BudgeteerModel

class PasswordTokenRecovery(ndb.Model):
    token = ndb.StringProperty()
    budgeteerKey = ndb.KeyProperty()

    @staticmethod
    def addTokenToDataStore(budgeteerId):
        tok = PasswordTokenRecovery()
        tok.token = PasswordTokenRecovery.generateToken(budgeteerId)
        tok.budgeteerKey = BudgeteerModel.Budgeteer.getBudgeteerById(budgeteerId).key
        tok.put()
        return tok.key.id()

    @staticmethod
    def generateToken(budgeteerId):
        m = hashlib.md5()
        m.update(str(budgeteerId) + str(datetime.now()))
        return m.hexdigest()

    @staticmethod
    def getTokenByBudgeteerId(budgeteerId):
        budgeteerKey = BudgeteerModel.Budgeteer.getBudgeteerById(budgeteerId).key
        if not budgeteerKey:
            return None
        tok = PasswordTokenRecovery.query(PasswordTokenRecovery.budgeteerKey == budgeteerKey).get()
        if tok:
            return tok.token
        return None

    @staticmethod
    def resetPassword(tokenId):
        rst = PasswordTokenRecovery.query(PasswordTokenRecovery.token == tokenId).get()
        if rst:
            PasswordTokenRecovery.removeToken(rst)
            return rst.budgeteerKey.id()
        return None

    @staticmethod
    def removeToken(token):
        token.key.delete()
