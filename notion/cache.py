from typing import Any
from .page import Page
from .database import Database


class Cache:
    """
    simple setter and getter to prevent exceeding rate limits
    """

    def __init__(self):
        self.pages = CachedObjects(valid_types=(Page), parent=self)
        self.databases = CachedDbObjects(valid_types=(Database), parent=self)
        self.columns = DbColumnsRegister()
        self.client = None

    def __repr__(self):
        return f"<notion.Cache; pages: {self.pages.objects}, databases: {self.databases.objects}>"


class CachedObjects:

    def __init__(self, valid_types, parent):
        self.parent= parent
        self.valid_types = valid_types
        self.objects = dict()

    def add(self, obj):
        if not isinstance(obj, self.valid_types):
            raise TypeError(
                f"No valid object was provided to cache.\nAcceptable: {self.valid_types},  provided: {type(obj)}")
        self.objects[str(obj.model.id).replace("-", "")] = obj

    def get(self, obj_id):
        try:
            return self.objects[obj_id.replace("-", "")]
        except KeyError:
            return None

    def __contains__(self, obj_id):
        return self.get(obj_id) is not None

class CachedDbObjects(CachedObjects):

    def add(self, obj):
        super().add(obj)
        for c in obj.properties.values():
            self.parent.columns.add()

class DbColumnsRegister:

    def __init__(self) -> None:
        self.columns = dict()

    def add(self, column):
        self.columns[column.id] = column

    def get(self, id):
        try:
            return self.columns[id]
        except KeyError:
            return None

    def __getattr__(self, v):
        return self.get(v)


cache = Cache()
