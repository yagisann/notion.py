"""
Page property objects
This model can be used in GET page requests

https://developers.notion.com/reference/property-value-object
"""
from notion.base_model import Connect
from pydantic import EmailStr, HttpUrl
from .base_model import NotionObjectModel, NotionBaseModel
from .base_object import DateObject, SelectOption, SelectOptionList, OptionGroup, StatusOptions
from .user import User
from .file import File
from .rich_text import RichText as RichTextPayload
from typing import Literal, Union
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

    def __init__(self, connect: Connect = None, **kwargs) -> None:
        super().__init__(connect, **kwargs)
        self.belong_to = None
        self.find_column()

    def get_value(self):
        return self.__getattribute__(self.type)
    
    def build(self):
        return self.model_dump()
    
    def find_column(self):
        from .cache import cache
        self.belong_to = cache.columns.get(self.id)


class CreatedBy(BasePageProperty):
    """ uneditable """
    type: Literal["created_by"]
    created_by: User


class CreatedTime(BasePageProperty):
    """ uneditable """
    type: Literal["created_time"]
    created_time: dt


class LastEditedBy(BasePageProperty):
    """ uneditable """
    type: Literal["last_edited_by"]
    last_edited_by: User


class LastEditedTime(BasePageProperty):
    """ uneditable """
    type: Literal["last_edited_time"]
    last_edited_time: dt


class MultiSelect(BasePageProperty):
    type: Literal["multi_select"]
    multi_select: list[SelectOption]

    def get_value(self):
        return [i.name for i in super().get_value()]


class Select(BasePageProperty):
    type: Literal["select"]
    select: SelectOption | None

    def get_value(self):
        val = super().get_value()
        return None if val is None else val.name


class Status(BasePageProperty):
    type: Literal["status"]
    status: SelectOption | None

    def get_value(self):
        val = super().get_value()
        return None if val is None else val.name


class Title(BasePageProperty):
    type: Literal["title"]
    title: list[RichTextPayload]

    def get_value(self):
        return "".join([i.plain_text for i in super().get_value()])


class RichText(BasePageProperty):
    type: Literal["rich_text"]
    rich_text: list[RichTextPayload]

    def get_value(self):
        return "".join([i.plain_text for i in super().get_value()])


class Relation(BasePageProperty):
    type: Literal["relation"]
    has_more: bool
    # page relation object that contain id of page
    relation: list[NotionObjectModel]


class Rollup(BasePageProperty):
    type: Literal["rollup"]
    # TODO


class Checkbox(BasePageProperty):
    type: Literal["checkbox"]
    checkbox: bool


class Date(BasePageProperty):
    type: Literal["date"]
    date: DateObject | None


class Email(BasePageProperty):
    type: Literal["email"]
    email: EmailStr | None


class Files(BasePageProperty):
    type: Literal["files"]
    files: list[File]


class Formula(BasePageProperty):
    """ uneditable """
    type: Literal["formula"]
    formula: FormulaValues


class Number(BasePageProperty):
    type: Literal["number"]
    number: int | float | None


class People(BasePageProperty):
    type: Literal["people"]
    people: list[User]


class PhoneNumber(BasePageProperty):
    type: Literal["phone_number"]
    phone_number: str | None


class Url(BasePageProperty):
    type: Literal["url"]
    url: HttpUrl | None

    def get_value(self):
        return str(super().get_value())


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
