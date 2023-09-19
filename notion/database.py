"""
Database objects

https://developers.notion.com/reference/database
"""
from __future__ import annotations

from pydantic import HttpUrl, Field, BaseModel
from .base_model import NotionObjectModel
from .exceptions import NotionValidationError
from .rich_text import RichText, Text
from .parent import Parent, DatabaseParent, PageParent, BlockParent
from .page import Page
from .user import User
from .file import ExternalFile, File
from .emoji import Emoji
from .database_property import DatabaseProperty

import emoji
from urllib.parse import urlparse
from typing import Literal, Any, TYPE_CHECKING
from datetime import datetime as dt

if TYPE_CHECKING:
    from .draft import PageDraft


__all__ = (
    "Database",
)

class Database(NotionObjectModel):
    object: Literal["database"]
    created_time: dt
    created_by: User
    last_edited_time: dt
    last_edited_by: User
    title: list[RichText]
    description: list[RichText]
    icon: File | Emoji | None
    cover: ExternalFile | None
    parent: Parent
    url: HttpUrl
    archived: bool
    is_inline: bool
    public_url: None | HttpUrl
    properties: dict[str, DatabaseProperty]

    pages: dict[Any, Any] = Field(default=dict(), exclude=True)

    def __init__(self, *, client, **kwargs):
        super().__init__(**kwargs)
        self.client = client
        self.cache = client.cache
        self.cache.databases.add(self)
        self.page_key_callback = lambda page: page.id

    def __getitem__(self, v):
        try:
            return self.properties[v]
        except KeyError:
            raise KeyError(
                f"'{self.__class__.__name__}' instance has no property named '{v}'")
    
    def _parse(self, data):
        for field in self.model_fields.keys():
            if data.get(field):
                self.__setattr__(field, data.get(field))

    def edit(
        self,
        *,
        title: str = Ellipsis,
        description: str = Ellipsis,
        icon: str = Ellipsis,
        cover: str = Ellipsis,
        is_inline: bool = Ellipsis,
    ):
        excpt = []
        if title is not Ellipsis:
            if isinstance(title, str):
                self.title = [Text.new(text=title)]
            else:
                excpt.append(TypeError("title sould be str."))
        if description is not Ellipsis:
            if isinstance(description, str):
                self.description = [Text.new(text=description)]
            else:
                excpt.append(TypeError("description sould be str."))
        if icon is not Ellipsis:
            if isinstance(icon, str):
                if emoji.is_emoji(icon):
                    self.emoji = Emoji.new(emoji=icon)
                elif len(urlparse(icon).scheme):
                    self.emoji = ExternalFile.new(url=icon)
                else:
                    excpt.append(ValueError(
                        "Provided string is not valid url or emoji"))
            else:
                excpt.append(TypeError("icon sould be str."))
        if cover is not Ellipsis:
            if isinstance(icon, str):
                if len(urlparse(cover).scheme):
                    self.cover = ExternalFile.new(url=cover)
                else:
                    excpt.append(ValueError(
                        "Provided string is not valid url"))
            else:
                excpt.append(TypeError("cover sould be str."))
        if is_inline is not Ellipsis:
            self.is_inline = bool(is_inline)

        if excpt:
            ex = "Some error(s) occured. See below\n"
            for i in excpt:
                ex += f"{i.__class__.__name__}:\n    {i}\n"
            raise NotionValidationError(ex)

        return self

    def add_property(self, name, column):
        if not isinstance(name, str):
            raise TypeError("name should be string")
        if not isinstance(column, DatabaseProperty):
            raise TypeError("property should be proper DatabaseProperty")
        column.is_modified = True
        self.properties[name] = column
        return self

    async def update(
        self,
        *,
        title: str = Ellipsis,
        description: str = Ellipsis,
        icon: str = Ellipsis,
        cover: str = Ellipsis,
        is_inline: bool = Ellipsis,
    ):
        """ push the change of this database."""
        self.edit(title=title, description=description, icon=icon, cover=cover, is_inline=is_inline)
        properties = {}
        for name, column in self.properties.items():
            column.check_is_modified()
            if column.is_modified:
                properties[name] = column.build
        dump = self.model_dump()
        payload = {
            "database_id": dump["id"],
            "title": dump["title"],
            "description": dump["description"],
            "icon": dump["icon"],
            "cover": dump["cover"],
            "is_inline": dump["is_inline"],
            "properties": properties
        }
        response = await self.client.databases.update(**payload)
        self._parse(response)
        return self

    async def fetch_child_pages(self):
        next_cursor = None
        while True:
            payload = {"database_id": self.id}
            if next_cursor:
                payload["start_cursor"] = next_cursor
            query = await self.client.databases.query(**payload)
            for page_payload in query["results"]:
                page = Page(client=self.client, **page_payload)
                self.pages[self.page_key_callback(page)] = page
            if not query["has_more"]:
                break
            next_cursor = query["next_cursor"]
        return self

    async def create_page(
        self,
        draft: PageDraft
    ):
        draft.parent = self
        page = await self.client.create_page(draft=draft)
        self.pages[self.page_key_callback(page)] = page
        return page

    async def reload(self):
        """ reload database. """
        response = await self.client.databases.retrieve(database_id=self.id)
        self._parse(response)
        self.pages = {}
        await self.fetch_child_pages()
        return self