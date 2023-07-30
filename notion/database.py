from .models import Database as DatabaseModel
from .page import Page
from .builders import (
    DatabaseBuilder,
    DatabasePropertyBuilder,
    DatabaseParentBuilder,
    PageBuilder,
    PagePropertyBuilder,
)

class Database:

    def __init__(self, *, client, data):
        self.client = client
        self.model = DatabaseModel(**data)
        self.client.cache.databases.add(self)
        self.properties = self.model.properties
    
    def __getattr__(self, key):
        model_dict = self.model.model_dump()
        if key in model_dict:
            return model_dict[key]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")
    
    def __getitem__(self, key):
        model_dict = self.model.model_dump()["properties"]
        if key in model_dict:
            return model_dict[key]
        raise KeyError(f"'{self.__class__.__name__}' instance has no property named '{key}'")
        
    def __setitem__(self, key, val):
        raise NotImplementedError()


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
        new_model_data = await self.client.databases.update(**payload)
        self.model = DatabaseModel(**new_model_data)
    
    async def create_page(self, builder=None, properties=None):
        if not isinstance(builder, (PageBuilder)):
            raise TypeError("builder argument must be object of PageBuilder")
        if not isinstance(properties, (PagePropertyBuilder)):
            raise TypeError("properties argument must be object of PagePropertyBuilder")
        payload = builder.build()
        payload["properties"] = properties.build()
        payload["parent"] = DatabaseParentBuilder(database_id=str(self.model.id)).build()
        data = await self.client.pages.create(**payload)
        return Page(data=data, client=self.client)
        