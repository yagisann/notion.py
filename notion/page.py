"""
Page objects

https://developers.notion.com/reference/page
"""

from pydantic import HttpUrl, Field
from .base_model import NotionObjectModel
from .exceptions import NotionValidationError
from .parent import Parent
from .user import User
from .file import ExternalFile
from .emoji import Emoji
from typing import Literal, Any
from datetime import datetime as dt
from .page_property import PageProperty

import emoji
from urllib.parse import urlparse

__all__ = (
    "Page",
)


class Page(NotionObjectModel):
    object: Literal["page"]
    created_time: dt
    created_by: User
    last_edited_time: dt
    last_edited_by: User
    archived: bool
    icon: None | ExternalFile | Emoji
    cover: None | ExternalFile
    parent: Parent
    url: HttpUrl
    public_url: None | HttpUrl
    properties: dict[str, PageProperty]

    client: Any = Field(default=None, exclude=True, repr=False)
    cache: Any = Field(default=None, exclude=True, repr=False)

    def __init__(self, *, client, **kwargs):
        super().__init__(**kwargs)
        self.client = client
        self.cache = client.cache
        self.cache.pages.add(self)
        for prop in self.properties.values():
            prop.set_parent(self)

    async def get_paginated_items(self):
        for prop in self.properties.values():
            if prop.is_paginated:
                await prop.get_paginated_items()
        return self
    
    def get_property_values(self):
        return {i: j.get_value() for i, j in self.properties.items()}

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
    
    def get_title(self):
        return [i.get_value() for i in self.properties.values() if i.type=="title"][0]

    def edit(
        self,
        *,
        title: str = Ellipsis,
        archived: bool = Ellipsis,
        icon: str = Ellipsis,
        cover: str = Ellipsis,
    ):
        excpt = []
        if title is not Ellipsis:
            if isinstance(title, str):
                [i for i in self.properties.values() if i.type == "title"][0].set_text(title)
            else:
                excpt.append(TypeError("title sould be str."))
        if archived is not Ellipsis:
            self.archived = bool(archived)
        if icon is not Ellipsis:
            if isinstance(icon, str):
                if emoji.is_emoji(icon):
                    self.icon = Emoji.new(emoji=icon)
                elif len(urlparse(icon).scheme):
                    self.icon = ExternalFile.new(url=icon)
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

        if excpt:
            ex = "Some error(s) occured. See below\n"
            for i in excpt:
                ex += f"{i.__class__.__name__}:\n    {i}\n"
            raise NotionValidationError(ex)

        return self
    
    async def update(
        self,
        *,
        title: str = Ellipsis,
        archived: bool = Ellipsis,
        icon: str = Ellipsis,
        cover: str = Ellipsis,
    ):
        self.edit(title=title, archived=archived, icon=icon, cover=cover)
        properties = {}
        for name, column in self.properties.items():
            if column.is_modified:
                properties[name] = column.build()
        dump = self.model_dump()
        payload = {
            "page_id": dump["id"],
            "archived": dump["archived"],
            "icon": dump["icon"],
            "cover": dump["cover"],
            "properties": properties
        }
        response = await self.client.pages.update(**payload)
        self._parse(response)
        return self

    async def reload(self):
        response = await self.client.pages.retrieve(page_id=self.id)
        self._parse(response)
        return self
    
    async def archive(self):
        payload = {
            "page_id": self.id,
            "archived": True,
        }
        response = await self.client.pages.update(**payload)
        self._parse(response)
        return self
    
    async def restore(self):
        payload = {
            "page_id": self.id,
            "archived": False,
        }
        response = await self.client.pages.update(**payload)
        self._parse(response)
        return self
    

