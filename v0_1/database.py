from .models import Database as DatabaseModel
from .page import Page
from .builders import (
    DatabaseBuilder,
    DatabasePropertyBuilder,
    DatabaseParentBuilder,
    PageBuilder,
    PagePropertyBuilder,
)
from.utils import NotionObject

class Database(NotionObject):

    def __init__(self, *, client, data):
        super().__init__()
        self.client = client
        self.model_dict = data
        self.model = DatabaseModel(**data)
        self.client.cache.databases.add(self)
        self.properties = self.model.properties
        self.pages = dict()
        self.page_key_callback = lambda page: page.id
        self.initialized=True

    def __getattr__(self, key):
        try:
            return super().__getattribute__(key)
        except AttributeError:
            if key in self.model_dict:
                return self.model_dict[key]
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")
    
    def __getitem__(self, key):
        if key in self.model_dict["properties"]:
            return self.model_dict["properties"][key]
        raise KeyError(f"'{self.__class__.__name__}' instance has no property named '{key}'")

    def __setattr__(self, key, val):
        if not self.initialized:
            super().__setattr__(key, val)
            return
        if key in self.model_dict:
            return NotImplementedError()
        super().__setattr__(key, val)
        
    def __setitem__(self, key, val):
        raise NotImplementedError()
    

    async def update(self):
        self.model_dict = await self.client.databases.retrieve(database_id=self.id)
        self.model = DatabaseModel(**self.model_dict)
        return self

    async def edit(self, builder=None, properties=None):
        if not isinstance(builder, (DatabaseBuilder, type(None))):
            raise TypeError("builder argument must be object of DatabaseBuilder")
        if not isinstance(properties, (DatabasePropertyBuilder, type(None))):
            raise TypeError("properties argument must be object of DatabasePropertyBuilder")
        if not (builder or properties):
            return
        payload = {"database_id": self.model.id}
        if builder:
            payload.update(builder.build())
        if properties:
            payload["properties"] = properties.build()
        self.model_dict = await self.client.databases.update(**payload)
        self.model = DatabaseModel(**self.model_dict)
        return self
    
    async def create_page(self, builder=None, properties=None):
        if not isinstance(builder, (PageBuilder)):
            raise TypeError("builder argument must be object of PageBuilder")
        if not isinstance(properties, (PagePropertyBuilder)):
            raise TypeError("properties argument must be object of PagePropertyBuilder")
        payload = builder.build()
        payload["properties"] = properties.build()
        payload["parent"] = DatabaseParentBuilder(database_id=str(self.model.id)).build()
        data = await self.client.pages.create(**payload)
        page = Page(data=data, client=self.client)
        self.pages[self.page_key_callback(page)] = page
        return page
    
    def set_page_key_callback(self, callback):
        self.page_key_callback = callback
        self.pages = {callback(page): page for page in self.pages.values()}
        return self
    
    async def fetch_pages(self, filter=None):
        next_cursor = None
        while True:
            payload = {"database_id": self.id}
            if next_cursor:
                payload["start_cursor"] = next_cursor
            query = await self.client.databases.query(**payload)
            for page_payload in query["results"]:
                page = Page(data=page_payload, client=self.client)
                self.pages[self.page_key_callback(page)] = page
            if not query["has_more"]:
                break
            next_cursor = query["next_cursor"]
        return self
    