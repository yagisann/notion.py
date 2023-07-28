"""
the definition of object that frequently appears in Notion API.
"""

from pydantic import EmailStr, HttpUrl
from .base_model import NotionBaseModel
from .enums import Color
from datetime import datetime as dt

__all__ = (
    "UrlObject",
    "DateObject",
    "EmailObject",
    "EmptyObject",
)

class UrlObject(NotionBaseModel):
    url: HttpUrl

class DateObject(NotionBaseModel):
    start: None | dt
    end: None | dt
    time_zone: None | str

class EmailObject(NotionBaseModel):
    email: EmailStr

class EmptyObject(NotionBaseModel, extra="forbid"):
    ...

class SelectOption(NotionBaseModel):
    id: str
    name: str
    color: Color

class OptionGroup(NotionBaseModel):
    id: str
    name: str
    color: Color
    option_ids: list[str]

class SelectOptionList(NotionBaseModel):
    options: list[SelectOption]
    
class StatusOptions(NotionBaseModel):
    options: list[SelectOption]
    groups: list[OptionGroup]