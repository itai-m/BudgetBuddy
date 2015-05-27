from google.appengine.ext import ndb
import hashlib
from datetime import datetime
import BudgeteerModel

class PasswordTokenRecovery(ndb.Model):
    token = ndb.StringProperty()
    budgeteerId = ndb.KeyProperty()

    @staticmethod
    def addTokenToDataStore(budgeteerId):
        tok = PasswordTokenRecovery()
        tok.token = PasswordTokenRecovery.generateToken(budgeteerId)
        tok.budgeteerId = budgeteerId
        tok.put()
        return tok.key.id()

    @staticmethod
    def generateToken(budgeteerId):
        m = hashlib.md5()
        m.update(str(budgeteerId) + str(datetime.now()))
        return m.hexdigest()

    @staticmethod
    def resetPassword(budgeteerId, tokenId):
        rst = PasswordTokenRecovery.query(PasswordTokenRecovery.token == tokenId, PasswordTokenRecovery.budgeteerId == budgeteerId).get()
        if rst:
            PasswordTokenRecovery.removeToken(rst)
            return True
        return False

    @staticmethod
    def removeToken(token):
        token.key.delete()
