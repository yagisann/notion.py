from __future__ import annotations

from .base_model import NotionBaseModel
from .database import Database
from .database_property import DatabaseProperty
from .emoji import Emoji
from .exceptions import NotionValidationError
from .file import File, ExternalFile
from .page import Page
from .page_property import PageProperty, name_class_link
from .parent import Parent, DatabaseParent, PageParent, BlockParent
from .rich_text import RichText, Text

from pydantic import field_validator, HttpUrl
import emoji
from typing import Literal
from urllib.parse import urlparse

class DatabaseDraft(NotionBaseModel):
    title: str | RichText | list[RichText]
    parent: Parent | Database | Page = None
    object: Literal["database"] = "database"
    description: str | RichText | list[RichText] = ""
    icon: str | File | Emoji | None = None
    cover: str | ExternalFile | None = None
    is_inline: bool = True
    properties: dict[str, DatabaseProperty] = {}

    @field_validator("parent")
    @classmethod
    def parent_validate(cls, value):
        if isinstance(value, Database):
            return DatabaseParent.new(value.id)
        elif isinstance(value, Page):
            return PageParent.new(value.id)
        # TODO: elif isinnstance(value, Block):
        # TODO:     return BlockParent.new(value.id)
        return value

    @field_validator("title", "description")
    @classmethod
    def string_validate(cls, value):
        if isinstance(value, str):
            return [Text.new(text=value)]
        elif isinstance(value, RichText):
            return [value]
        return value

    @field_validator("icon")
    @classmethod
    def icon_validate(cls, value):
        if isinstance(value, str):
            if emoji.is_emoji(value):
                return Emoji.new(emoji=value)
            elif len(urlparse(value).scheme):
                return ExternalFile.new(url=value)
        return value

    @field_validator("cover")
    @classmethod
    def cover_validate(cls, value):
        if isinstance(value, str):
            if len(urlparse(value).scheme):
                return ExternalFile.new(url=value)
        return value

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

    async def create(self, client):
        db = await client.create_database(draft=self)
        return db

class PageDraft(NotionBaseModel):
    title: str | RichText | list[RichText]
    object: Literal["page"] = "page"
    archived: bool = False
    icon: None | ExternalFile | Emoji | str = None
    cover: None | ExternalFile | str = None
    parent: Parent | Database | Page = None
    properties: dict[str, PageProperty] = {}

    parent_database: Database = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.parent_database is None:
            if title_column := [(i,j) for i, j in self.properties.items() if j.type == "title"]:
                self.properties[title_column[0][0]].title = self.title
            else:
                self.properties["title"].title = self.title
        else:
            generated = self.generate_properties_from(self.parent_database)
            self.properties = generated
            [i for i in self.properties.items() if i.type == "title"][0].title = self.title
    
    @staticmethod
    def generate_properties_from(database: Database):
        generated = {}
        for name, column in database.properties.items():
            target_class = name_class_link[column.type]
            if not target_class.model_fields["editable"].default:
                continue
            generated[name] = target_class.new(id=column.id)
        return generated


    @field_validator("parent")
    @classmethod
    def parent_validate(cls, value):
        if isinstance(value, Database):
            return DatabaseParent.new(value.id)
        elif isinstance(value, Page):
            return PageParent.new(value.id)
        # TODO: elif isinnstance(value, Block):
        # TODO:     return BlockParent.new(value.id)
        return value

    @field_validator("title")
    @classmethod
    def string_validate(cls, value):
        if isinstance(value, str):
            return [Text.new(text=value)]
        elif isinstance(value, RichText):
            return [value]
        return value

    @field_validator("icon")
    @classmethod
    def icon_validate(cls, value):
        if isinstance(value, str):
            if emoji.is_emoji(value):
                return Emoji.new(emoji=value)
            elif len(urlparse(value).scheme):
                return ExternalFile.new(url=value)
        return value

    @field_validator("cover")
    @classmethod
    def cover_validate(cls, value):
        if isinstance(value, str):
            if len(urlparse(value).scheme):
                return ExternalFile.new(url=value)
        return value

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

        if excpt:
            ex = "Some error(s) occured. See below\n"
            for i in excpt:
                ex += f"{i.__class__.__name__}:\n    {i}\n"
            raise NotionValidationError(ex)

        return self