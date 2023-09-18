"""
the definition of object that frequently appears in Notion API.
"""

from pydantic import EmailStr, HttpUrl, BaseModel
from .base_model import NotionBaseModel
from .enums import Color
from .exceptions import UnUpdatableError
from typing import Literal, Any
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

    @classmethod
    def new(
        cls,
        start: None | dt = None,
        end: None | dt = None,
        time_zone: None | str = None,
        ):
        return cls(start=start, end=end, time_zone=time_zone)

class EmailObject(NotionBaseModel):
    email: EmailStr

class EmptyObject(BaseModel, extra="forbid"):
    ...

class PartialSelectOption(NotionBaseModel):
    name: str
    color: None | Color = None

    def __eq__(self, other):
        if isinstance(other, (PartialSelectOption,)):
            return self.name == other.name
        return NotImplemented

    def build(self):
        p = {"name": self.name}
        if self.color is not None:
            p["color"] = self.color.value
        return p

class SelectOption(PartialSelectOption):
    id: str
    color: Color

    def build(self):
        return self.model_dump(exclude={"id"})

class PartialOptionGroup(NotionBaseModel):
    name: str
    color: None | Color = None
    option_ids: list[str] = []

    def __eq__(self, other):
        if isinstance(other, (PartialOptionGroup,)):
            return self.name == other.name
        return NotImplemented
    
    def build(self):
        p = {"name": self.name, "option_ids": self.option_ids}
        if self.color is not None:
            p["color"] = self.color.value
        return p

class OptionGroup(NotionBaseModel):
    id: str
    name: str
    color: Color
    option_ids: list[str]

    def build(self):
        return self.model_dump(exclude={"id"})

class SelectOptionList(NotionBaseModel):
    options: list[SelectOption]

    def get(self, name: str):
        s = [op for op in self.options if op.name==name]
        return s[0] if len(s) else None
    
    def delete(self, name: str):
        s = self.get(name)
        try:
            self.options.remove(s)
        except ValueError:
            pass

    def append(
            self,
            name: str,
            color: None | Color = None
            ):
        s = self.get(name)
        if s is None:
            self.options.append(PartialSelectOption(name=name, color=color))
        elif isinstance(s, PartialSelectOption):
            s.color = color
        else:
            raise UnUpdatableError("Existing select option cannot be updated.")
    
    def build(self):
        return {"options": [op.build() for op in self.options]}
    
    @classmethod
    def new(cls):
        return cls(options=[])
    
class StatusOptions(NotionBaseModel):
    options: list[SelectOption]
    groups: list[OptionGroup]

    def get_option(self, name: str):
        s = [op for op in self.options if op.name==name]
        return s[0] if len(s) else None
    
    def delete_option(self, name: str):
        raise UnUpdatableError("Status cannot be updated via API")
    
    def add_option(self, group: str, name: str, color: None | Color):
        raise UnUpdatableError("Status cannot be updated via API")
    
    def get_group(self, name):
        s = [gr for gr in self.groups if gr.name==name]
        return s[0] if len(s) else None
    
    def delete_group(self, name):
        raise UnUpdatableError("Status cannot be updated via API")
    
    def append_group(self, name: str, color: None | Color = None, option_ids: list=[]):
        raise UnUpdatableError("Status cannot be updated via API")
    
    @classmethod
    def new(cls):
        return {}

class ArrayTypeObject(NotionBaseModel):
    type: Literal["array"]
    array: list[Any]

class ListObject(NotionBaseModel):
    """ pagenation objects"""
    object: Literal["list"]
    results: list[Any]
    next_cursor: None | HttpUrl
    has_more: bool