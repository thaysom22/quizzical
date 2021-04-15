### Helper classes, methods and constants ###
from bson.objectid import ObjectId
from flask import url_for

### REMOVE
def build_category_urls():
    """
    builds dict of urls to category images
    """
    CATEGORY_IMG_URLS = {
        "General Knowledge": url_for('static', filename='img/smiling-teacher.jpg') # test
    }

    return CATEGORY_IMG_URLS


class ObjectIdHelper():
    """
    class with static methods to convert to/from bson.objectId type
    """
    @staticmethod
    def fromObjectId(value):
        """
        if value is ObjectId convert it to string
        """
        if isinstance(value, ObjectId):
            return str(value)

    @staticmethod
    def toObjectId(value):
        """
        if value is string and valid convert it to ObjectId
        """
        if isinstance(value, str) and ObjectId.is_valid(value):
            return  ObjectId(value)
    

