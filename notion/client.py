from .notion_client import AsyncClient
from .database import Database
from .page import Page
from .builders import (
    DatabaseBuilder,
    DatabasePropertyBuilder,
    DatabaseParentBuilder,
    PageBuilder,
    PagePropertyBuilder,
    PageParentBuilder,
)
from .cache import cache

class Client:

    def __init__(self, token):
        self.token = token
        self.client = AsyncClient(auth=token)
        self.client.cache = cache
        self.cache = self.client.cache
    
    async def fetch_database(self, database_id: str) -> Database:
        if database_id in self.cache.databases:
            return self.cache.databases.get(database_id)
        data = await self.client.databases.retrieve(database_id=database_id)
        return Database(data=data, client=self.client)
    
    async def create_database(
        self,
        builder: DatabaseBuilder,
        properties: DatabasePropertyBuilder,
        parent: PageParentBuilder,
    ) -> Database:
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


    async def fetch_page(self, page_id: str) -> Page:
        if page_id in self.cache.pages:
            return self.cache.pages.get(page_id)
        data = await self.client.pages.retrieve(page_id=page_id)
        return Page(data=data, client=self.client)
    
    async def create_page(
        self,
        builder: PageBuilder,
        properties: PagePropertyBuilder,
        parent: DatabaseParentBuilder | PageParentBuilder,
    ) -> Page:
        if not isinstance(builder, (PageBuilder)):
            raise TypeError("builder argument must be object of PageBuilder")
        if not isinstance(properties, (PagePropertyBuilder)):
            raise TypeError("properties argument must be object of PagePropertyBuilder")
        if not isinstance(parent, (DatabaseParentBuilder, PageParentBuilder)):
            raise TypeError("parent argument must be object of DatabaseParentBuilder or PageParentBuilder")
        payload = builder.build()
        payload["properties"] = properties.build()
        payload["parent"] = parent.build()
        data = await self.client.pages.create(**payload)
        return Page(data=data, client=self.client)