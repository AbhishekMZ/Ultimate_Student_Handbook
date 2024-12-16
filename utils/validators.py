# utils/validators.py

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

class MongoValidator:
    @staticmethod
    def validate_object_id(id_string):
        try:
            return ObjectId.is_valid(id_string)
        except:
            return False

    @staticmethod
    def handle_mongo_errors(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except DuplicateKeyError:
                raise ValueError("Duplicate entry found")
            except Exception as e:
                raise Exception(f"Database error: {str(e)}")
        return wrapper