from .database import Database
from .page import Page

__all__ = (Cache,)

class Cache:
    """
    simple setter and getter to prevent exceeding rate limits
    """
    def __init__(self):
        self.pages = CachedObjects(valid_types=(Page,))
        self.databases = CachedObjects(valid_types=(Database,))
    
    
class CachedObjects:

    def __init__(self, valid_types):
        self.valid_types = valid_types
        self.objects = dict()
    
    def add(self, obj):
        if not isinstance(obj, self.valid_types):
            raise TypeError(f"No valid object was provided to cache.\nAcceptable: {self.valid_types},  provided: {type(obj)}")
        self.objects[str(obj.model.id).replace("-", "")] = obj
    
    def get(self, id):
        try:
            return self.object[str(obj.model.id).replace("-", "")]
        except KeyError:
            return None

    def __contains__(self, id):
        return self.get is not None

