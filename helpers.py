### Helper classes and methods###
from bson.objectid import ObjectId


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
    

