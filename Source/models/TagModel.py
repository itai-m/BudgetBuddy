from google.appengine.ext import ndb

class Tag(ndb.Model):
    description = ndb.StringProperty()


    @staticmethod 
    def getTag(tagKey):
        return Tag.query(Tag.key == tagKey)

    @staticmethod
    def addTag(tag):
        tag.put()
    
    @staticmethod
    def removeTag(tag):
        tag.key.delete()
