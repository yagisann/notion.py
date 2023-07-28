from .models import Database as DatabaseModel
from .builders import DatabaseBuilder, DatabasePropertyBuilder


class Database:

    def __init__(self, *, client, data):
        self.client = client
        self.model = DatabaseModel(**data)

    async def edit(self, builder=None, properties=None):
        if not isinstance(builder, (DatabaseBuilder, type(None))):
            raise TypeError("builder argument must be object of DatabaseBuilder")
        if not isinstance(properties, (DatabasePropertyBuilder, type(None))):
            raise TypeError("properties argument must be object of DatabasePropertyBuilder")
        payload = {"database_id": self.model.id}
        if builder:
            payload.update(builder.build())
        if properties:
            payload["properties"] = properties.build()
        new_model_data = await self.client.databases.update(**payload)
        self.model = DatabaseModel(**new_model_data)
        