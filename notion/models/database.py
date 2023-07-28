"""
Database objects

https://developers.notion.com/reference/database
"""

from pydantic import HttpUrl
from .base_model import NotionObjectModel
from .rich_text import RichText
from .parent import Parent
from .user import User
from .file import ExternalFile, File
from .emoji import Emoji
from typing import Literal
from datetime import datetime as dt

from .database_property import DatabaseProperty

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
