### Helper classes, methods and constants ###
from bson.objectid import ObjectId
from flask import url_for


def build_category_img_url(category_name):
    """
    build url to category image from category name
    """
    # make category_name url compatible
    filename = "img/categories/" + category_name.lower().replace(" ", "_") + ".jpg"  
    return url_for('static', filename=filename)


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
    

