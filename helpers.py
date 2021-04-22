### Helper classes, methods and constants ###
from bson.objectid import ObjectId
from flask import url_for

### NOT REQUIRED ? ###

# def build_category_img_url(category_name):
#     """
#     build url to category image from category name
#     """
#     # make category_name url compatible
#     filename = "img/categories/" + category_name.lower().replace(" ", "-") + ".jpg"  
#     return url_for('static', filename=filename)


class ObjectIdHelper():
    """
    class with static methods to convert to/from bson.objectId type
    """
    @staticmethod
    def fromObjectId(value):
        """
        if value is ObjectId type convert it to string else leave unchanged
        """
        if isinstance(value, ObjectId):
            return str(value)
        
        return value

    @staticmethod
    def toObjectId(value):
        """
        if value is valid string convert it to ObjectId else leave unchanged
        """
        if isinstance(value, str) and ObjectId.is_valid(value):
            return  ObjectId(value)

        return value
    

