"""
Page objects

https://developers.notion.com/reference/page
"""

from pydantic import HttpUrl
from .base_model import NotionObjectModel
from .rich_text import RichText
from .parent import Parent
from .user import User
from .file import ExternalFile
from .emoji import Emoji
from typing import Literal
from datetime import datetime as dt

from .page_property import PageProperty

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
    icon: ExternalFile | Emoji
    cover: ExternalFile
    parent: Parent
    url: HttpUrl
    public_url: None | HttpUrl
    properties: dict[str, PageProperty]
