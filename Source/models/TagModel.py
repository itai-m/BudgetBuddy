from google.appengine.ext import ndb

class Tag(ndb.Model):
    description = ndb.StringProperty()

    @staticmethod
    def getTagByKey(tagKey):
        '''
        Receives a tag key, returns a Tag object.
        :param tagKey: tag key.
        :return: Tag object.
        '''
        return tagKey.get()

    @staticmethod
    def addTagToDatastore(tag):
        '''
        Adds a tag to the Datastore, and returns the key.
        :param tag: Tag object.
        :return: Key to the datastore entry of the tag object.
        '''
        tag.put()
        return tag.key
    
    @staticmethod
    def removeTag(tag):
        '''
        Removes a tag from the datastore.
        :param tag: Tag object.
        :return: None
        '''
        tag.key.delete()
        return None
