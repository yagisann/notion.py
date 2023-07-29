"""
Page property objects
This model can be used in GET page requests

https://developers.notion.com/reference/property-value-object
"""
from pydantic import EmailStr, HttpUrl
from .base_model import NotionObjectModel, NotionBaseModel
from .base_object import DateObject, SelectOption, SelectOptionList, OptionGroup, StatusOptions
from .user import User
from .file import File
from .rich_text import RichText as RichTextPayload
from .enums import Color
from typing import Literal, Union
from enum import Enum
from datetime import datetime as dt

class BoolFormulaValues(NotionBaseModel):
    type: Literal["boolean"]
    boolean: bool

class DateFormulaValues(NotionBaseModel):
    type: Literal["date"]
    date: dt

class NumberFormulaValues(NotionBaseModel):
    type: Literal["number"]
    number: int | float

class StringFormulaValues(NotionBaseModel):
    type: Literal["string"]
    string: str

FormulaValues = Union[
    BoolFormulaValues,
    DateFormulaValues,
    NumberFormulaValues,
    StringFormulaValues,
]


class BasePageProperty(NotionBaseModel):
    id: str


class CreatedBy(BasePageProperty):
    type: Literal["created_by"]
    created_by: User

class CreatedTime(BasePageProperty):
    type: Literal["created_time"]
    created_time: dt

class LastEditedBy(BasePageProperty):
    type: Literal["last_edited_by"]
    last_edited_by: User

class LastEditedTime(BasePageProperty):
    type: Literal["last_edited_time"]
    last_edited_time: dt

class MultiSelect(BasePageProperty):
    type: Literal["multi_select"]
    multi_select: SelectOptionList

class Select(BasePageProperty):
    type: Literal["select"]
    select: SelectOption

class Status(BasePageProperty):
    type: Literal["status"]
    status: SelectOption

class Title(BasePageProperty):
    type: Literal["title"]
    title: list[RichTextPayload]

class RichText(BasePageProperty):
    type: Literal["rich_text"]
    rich_text: list[RichTextPayload]

class Relation(BasePageProperty):
    type: Literal["relation"]
    has_more: bool
    relation: list[NotionObjectModel] # page relation object that contain id of page

class Rollup(BasePageProperty):
    type: Literal["rollup"]
    # TODO

class Checkbox(BasePageProperty):
    type: Literal["checkbox"]
    checkbox: bool

class Date(BasePageProperty):
    type: Literal["date"]
    date: DateObject

class Email(BasePageProperty):
    type: Literal["email"]
    email: EmailStr

class Files(BasePageProperty):
    type: Literal["files"]
    files: list[File]

class Formula(BasePageProperty):
    type: Literal["formula"]
    formula: FormulaValues

class Number(BasePageProperty):
    type: Literal["number"]
    number: int | float

class People(BasePageProperty):
    type: Literal["people"]
    people: list[User]

class PhoneNumber(BasePageProperty):
    type: Literal["phone_number"]
    phone_number: str

class Url(BasePageProperty):
    type: Literal["url"]
    url: HttpUrl


PageProperty = Union[
    Checkbox,
    CreatedBy,
    CreatedTime,
    Date,
    Email,
    Files,
    Formula,
    LastEditedBy,
    LastEditedTime,
    MultiSelect,
    Number,
    People,
    PhoneNumber,
    Relation,
    Rollup,
    RichText,
    Select,
    Status,
    Title,
    Url,
]