from .notion_client import AsyncClient
from .database import Database
from .builders import DatabaseBuilder, DatabasePropertyBuilder, PageParentBuilder
import logging

class Client:

    def __init__(self, token):
        self.token = token
        self.client = AsyncClient(auth=token)
    
    async def fetch_database(self, database_id: str) -> Database:
        data = await self.client.databases.retrieve(database_id=database_id)
        return Database(data=data, client=self.client)
    
    async def create_database(
        self,
        builder: DatabaseBuilder,
        properties: DatabasePropertyBuilder,
        parent: PageParentBuilder,
    ):
        if not isinstance(builder, (DatabaseBuilder)):
            raise TypeError("builder argument must be object of DatabaseBuilder")
        if not isinstance(properties, (DatabasePropertyBuilder)):
            raise TypeError("properties argument must be object of DatabasePropertyBuilder")
        if not isinstance(parent, (PageParentBuilder)):
            raise TypeError("parent argument must be object of PageParentBuilder")
        payload = builder.build()
        payload["properties"] = properties.build()
        payload["parent"] = parent.build()
        if "title" not in payload:
            raise ValueError(f"Database title should be specified.")
        data = await self.client.databases.create(**payload)
        return Database(data=data, client=self.client)

