from .database import Database
from .page import Page

class Cache:
    """
    simple setter and getter to prevent exceeding rate limits
    """
    def __init__(self):
        self.pages = CachedObjects(valid_types=(Page,))
        self.databases = CachedObjects(valid_types=(Database,))
    
    def __repr__(self):
        return f"<notion.Cache; pages: {self.pages.objects}, databases: {self.databases.objects}>"
    
    
class CachedObjects:

    def __init__(self, valid_types):
        self.valid_types = valid_types
        self.objects = dict()
    
    def add(self, obj):
        if not isinstance(obj, self.valid_types):
            raise TypeError(f"No valid object was provided to cache.\nAcceptable: {self.valid_types},  provided: {type(obj)}")
        self.objects[str(obj.model.id).replace("-", "")] = obj
    
    def get(self, obj_id):
        try:
            return self.objects[obj_id.replace("-", "")]
        except KeyError:
            return None

    def __contains__(self, obj_id):
        return self.get(obj_id) is not None

