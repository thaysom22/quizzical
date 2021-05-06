# HELPERS #

from bson.objectid import ObjectId


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
            return ObjectId(value)

        return value
