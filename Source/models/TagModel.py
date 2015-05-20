from google.appengine.ext import ndb

class Tag(ndb.Model):
    description = ndb.StringProperty()


    @staticmethod 
    def getTagDesc(tagKey):
        return Tag.query(Tag.key == tagKey)
    
    @statidmethod
    def insertTag(tag):
        tag.put()
    
    def removeTag(tag):
        tag.key.delete()

