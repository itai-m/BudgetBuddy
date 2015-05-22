from google.appengine.ext import ndb

class Tag(ndb.Model):
    description = ndb.StringProperty()

    @staticmethod
    def getTag(tagKey):
        return Tag.query(Tag.key == tagKey).get()

    @staticmethod
    def addTag(tag):
        tag.put()
        return tag.key.id()
    
    @staticmethod
    def removeTag(tag):
        tag.key.delete()
