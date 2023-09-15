"""
Page property objects
This model can be used in GET page requests

https://developers.notion.com/reference/property-value-object
"""
from __future__ import annotations
from notion.base_model import Connect
from pydantic import EmailStr, HttpUrl
from .exceptions import ClientMissingError
from .base_model import NotionObjectModel, NotionBaseModel
from .general_object import DateObject, PartialSelectOption, SelectOption, SelectOptionList, OptionGroup, StatusOptions
from .user import User
from .file import File
from .rich_text import Text, RichText as RichTextUnion
from .notion_client.helpers import query_finder
from typing import Literal, Union, TYPE_CHECKING
from datetime import datetime as dt

if TYPE_CHECKING:
    from .page import Page

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
    editable: bool = True

    def __init__(self, connect: Connect = None, parent: Page = None, **kwargs) -> None:
        super().__init__(connect, **kwargs)
        self.parent = parent
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
    editable: bool = False


class CreatedTime(BasePageProperty):
    """ uneditable """
    type: Literal["created_time"]
    created_time: dt
    editable: bool = False


class LastEditedBy(BasePageProperty):
    """ uneditable """
    type: Literal["last_edited_by"]
    last_edited_by: User
    editable: bool = False


class LastEditedTime(BasePageProperty):
    """ uneditable """
    type: Literal["last_edited_time"]
    last_edited_time: dt
    editable: bool = False


class MultiSelect(BasePageProperty):
    type: Literal["multi_select"]
    multi_select: list[SelectOption]

    def get_value(self):
        return [i.name for i in super().get_value()]
    
    def validate(self, options):
        if self.belong_to:
            col_options = self.belong_to.multi_select.options
            for op in options:
                if op not in col_options:
                    raise ValueError("invalid option name for this property. valid option names: "+str([i.name for i in col_options]))
    
    def set_options(self, options: list[str]):
        formed_options = []
        for op in options:
            if isinstance(op, PartialSelectOption):
                formed_options.append(op)
            elif isinstance(op, str):
                formed_options.append(PartialSelectOption(name=op))
            else:
                raise TypeError("options should be list of str, ParialSelectOption, SelectOption.")
        self.validate(formed_options)
        self.multi_select = formed_options


class Select(BasePageProperty):
    type: Literal["select"]
    select: SelectOption | None

    def get_value(self):
        val = super().get_value()
        return None if val is None else val.name

    def validate(self, option):
        if self.belong_to:
            col_options = self.belong_to.select.options
            if option not in col_options:
                raise ValueError("invalid option name for this property. valid option names: "+str([i.name for i in col_options]))
    
    def set_option(self, option: str):
        if isinstance(option, PartialSelectOption):
            formed_option = option
        elif isinstance(option, str):
            formed_option = PartialSelectOption(name=option)
        else:
            raise TypeError("options should be list of str, ParialSelectOption, SelectOption.")
        self.validate(formed_option)
        self.select = formed_option


class Status(BasePageProperty):
    type: Literal["status"]
    status: SelectOption | None

    def get_value(self):
        val = super().get_value()
        return None if val is None else val.name

    def validate(self, option):
        if self.belong_to:
            col_options = self.belong_to.status.options
            if option not in col_options:
                raise ValueError("invalid option name for this property. valid option names: "+str([i.name for i in col_options]))
    
    def set_status(self, option: str):
        if isinstance(option, PartialSelectOption):
            formed_option = option
        elif isinstance(option, str):
            formed_option = PartialSelectOption(name=option)
        else:
            raise TypeError("options should be list of str, ParialSelectOption, SelectOption.")
        self.validate(formed_option)
        self.status = formed_option


class Title(BasePageProperty):
    type: Literal["title"]
    title: list[RichTextUnion]

    def get_value(self):
        return "".join([i.plain_text for i in super().get_value()])
    
    def set_text(self, text: str):
        if isinstance(text, str):
            self.title = Text.new(text)
        elif isinstance(text, Text):
            self.title = text
        else:
            raise TypeError("text should be one of str, Text")


class RichText(BasePageProperty):
    type: Literal["rich_text"]
    rich_text: list[RichTextUnion]

    def get_value(self):
        return "".join([i.plain_text for i in super().get_value()])

    def set_text(self, text: str):
        if isinstance(text, str):
            self.title = Text.new(text)
        elif isinstance(text, RichTextUnion):
            self.title = text
        else:
            raise TypeError("text should be one of str, Text, MentionText, EquationText.")


class Relation(BasePageProperty):
    type: Literal["relation"]
    has_more: bool
    # page relation object that contain id of page
    relation: list[NotionObjectModel]

    async def get_pagenated_items(self):
        if not self.has_more:
            return
        if client:=self._connect.client is None:
            raise ClientMissingError()
        self.relation = []
        start_cursor = {}
        has_more = 1
        while has_more:
            r = await client.pages.properties.retrieve(page_id=self.parent.id, property_id=self.id, **start_cursor)
            for i in r["results"]:
                self.relation.append(NotionObjectModel(**i["relation"]))
            has_more = r["has_more"]
            start_cursor = query_finder(r["next_cursor"])


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
