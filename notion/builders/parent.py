from .base_builder import *
from ..models.parent import PageParent

class PageParentBuilder(BaseBuilder):
    fields_setting = {
        "page_id": {
            str: lambda x: PageParent(type="page_id", page_id=x),
            PageParent: lambda x: x
        }
    }

    def build(self):
        return self.fields_value["page_id"].model_dump()

class DatabaseParentBuilder(BaseBuilder):
    fields_setting = {
        "database_id": {
            str: lambda x: DatabaseParent(type="database_id", database_id=x),
            DatabaseParent: lambda x: x
        }
    }

    def build(self):
        return self.fields_value["database_id"].model_dump()