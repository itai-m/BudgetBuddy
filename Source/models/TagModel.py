from google.appengine.ext import ndb


'''
    Functionality tests:
        [X] Get Tag By Key
        [X] Add Tag To DS
        [X] Remove Tag From DS
'''


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
    def getTagKeyByName(tagname):
        '''
        Receives a tag name (supposed to be unique), returns the tag key.
        :param tagname: Tag name.
        :return: key of input tagname.
        '''
        tag = Tag.query(Tag.description == tagname).get()
        return tag.key

    @staticmethod
    def getAllTags():
        '''
        Returns all the tags in the database.
        :return: List of all tag objects in the database.
        '''
        return Tag.query().fetch()


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
