from .models import Database as DatabaseModel
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
        payload["parent"] = DatabaseParentBuilder(self.model.id).build()
        data = await self.client.pages.create(**payload)
        return Page(data=data, client=self.client)
        