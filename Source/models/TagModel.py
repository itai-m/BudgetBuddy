from google.appengine.ext import ndb

class Tag(ndb.Model):
    description = ndb.StringProperty()


    @staticmethod 
    def getTagDesc(tagkey):
        return Tag.query(Tag.key == tagkey)

