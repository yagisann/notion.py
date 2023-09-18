from .notion_client import AsyncClient
from .database import Database
from .database_property import DatabaseProperty
from .exceptions import FieldMissingError
from .page import Page
from .draft import DatabaseDraft, PageDraft
from .cache import cache
from .parent import Parent

class Client:

    def __init__(self, token, loglevel=20):
        self.token = token
        self.client = AsyncClient(auth=token, log_level=loglevel)
        self.client.cache = cache
        self.cache = self.client.cache
    
    async def fetch_database(self, database_id: str) -> Database:
        if database_id in self.cache.databases:
            return self.cache.databases.get(database_id)
        data = await self.client.databases.retrieve(database_id=database_id)
        return Database(client=self.client, **data)
    
    async def fetch_page(self, page_id: str) -> Page:
        if page_id in self.cache.pages:
            return self.cache.pages.get(page_id)
        data = await self.client.pages.retrieve(page_id=page_id)
        return Page(client=self.client, **data)
    
    async def create_database(
        self,
        draft: DatabaseDraft
    ) -> Database:
        if draft.parent is None:
            raise FieldMissingError("draft is missing 'parent' field")
        data = await self.client.databases.create(**draft.model_dump())
        return Database(client=self.client, **data)

    async def create_page(
        self,
        draft: PageDraft
    ) -> Page:
        if draft.parent is None:
            raise FieldMissingError("draft is missing 'parent' field")
        data = await self.client.pages.create(**draft.model_dump())
        return Page(client=self.client, **data)