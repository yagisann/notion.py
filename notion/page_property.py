"""
Page property objects
This model can be used in GET page requests

https://developers.notion.com/reference/property-value-object
"""
from __future__ import annotations
from pydantic import EmailStr, HttpUrl, Field
from .base_model import NotionObjectModel, NotionBaseModel
from .general_object import DateObject, PartialSelectOption, SelectOption, ArrayTypeObject
from .enums import RollupFunctionType
from .exceptions import UnUpdatableError
from .user import User
from .file import File, ExternalFile
from .rich_text import Text, RichText as RichTextUnion
from .utils import query_finder
from typing import Literal, Union, TYPE_CHECKING, Any
from datetime import datetime as dt, timedelta
from urllib.parse import urlparse

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

    editable: bool = Field(default=True, exclude=True)
    is_paginated: bool = Field(default=False, exclude=True)
    is_modified: bool = Field(default=False, exclude=True)
    initialized: bool = Field(default=False, exclude=True)
    parent: Any = Field(default=None, exclude=True, repr=False)
    belong_to: Any = Field(default=None, exclude=True, repr=False)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.find_column()
        self.initialized = True
    
    def __setattr__(self, key, value):
        if not self.editable and self.initialized:
            raise UnUpdatableError()
        if self.initialized:
            super().__setattr__("is_modified", True)
        if key != "is_modified":
            super().__setattr__(key, value)


    def get_value(self):
        return self.__getattribute__(self.type)

    def build(self):
        return self.model_dump()
    
    def set_parent(self, parent: Page):
        super().__setattr__("parent", parent)

    def find_column(self):
        if self.belong_to is None:
            from .cache import cache
            super().__setattr__("belong_to", cache.columns.get(self.id))


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
    multi_select: list[SelectOption | PartialSelectOption]

    def get_value(self):
        return [i.name for i in super().get_value()]

    def validate(self, options):
        if self.belong_to:
            col_options = self.belong_to.multi_select.options
            for op in options:
                if op not in col_options:
                    raise ValueError(
                        "invalid option name for this property. valid option names: "+str([i.name for i in col_options]))

    def set_options(self, options: list[str]):
        formed_options = []
        for op in options:
            if isinstance(op, PartialSelectOption):
                formed_options.append(op)
            elif isinstance(op, str):
                formed_options.append(PartialSelectOption(name=op))
            else:
                raise TypeError(
                    "options should be list of str, ParialSelectOption, SelectOption.")
        self.validate(formed_options)
        self.multi_select = formed_options
        self.is_modified = True
    
    @classmethod
    def new(cls, id: str, options: list[str]=[], belong_to: Any=None):
        c = cls(id=id, type="multi_select", multi_select=[], belong_to=belong_to)
        c.set_options(options)
        return c


class Select(BasePageProperty):
    type: Literal["select"]
    select: SelectOption | PartialSelectOption | None

    def get_value(self):
        val = super().get_value()
        return None if val is None else val.name

    def validate(self, option):
        if self.belong_to:
            col_options = self.belong_to.select.options
            if option not in col_options:
                raise ValueError(
                    "invalid option name for this property. valid option names: "+str([i.name for i in col_options]))

    def set_option(self, option: str):
        if isinstance(option, PartialSelectOption):
            formed_option = option
        elif isinstance(option, str):
            formed_option = PartialSelectOption(name=option)
        else:
            raise TypeError(
                "options should be list of str, ParialSelectOption, SelectOption.")
        self.validate(formed_option)
        self.select = formed_option
        self.is_modified = True

    @classmethod
    def new(cls, id: str, option: str=None, belong_to: Any=None):
        c = cls(id=id, type="select", select=None, belong_to=belong_to)
        if option is not None:
            c.set_option(option)
        return c

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
                raise ValueError(
                    "invalid option name for this property. valid option names: "+str([i.name for i in col_options]))

    def set_status(self, option: str):
        if isinstance(option, PartialSelectOption):
            formed_option = option
        elif isinstance(option, str):
            formed_option = PartialSelectOption(name=option)
        else:
            raise TypeError(
                "options should be list of str, ParialSelectOption, SelectOption.")
        self.validate(formed_option)
        self.status = formed_option
        self.is_modified = True

    @classmethod
    def new(cls, id: str, status: str=None, belong_to: Any=None):
        c = cls(id=id, type="status", status=None, belong_to=belong_to)
        if status is not None:
            c.set_status(status)
        return c
    

class Title(BasePageProperty):
    type: Literal["title"]
    title: list[RichTextUnion]

    def get_value(self):
        return "".join([i.plain_text for i in super().get_value()])

    def set_text(self, text: str):
        if isinstance(text, str):
            self.title = [Text.new(text)]
        elif isinstance(text, Text):
            self.title = [text]
        else:
            raise TypeError("text should be one of str, Text")
        self.is_modified = True

    @classmethod
    def new(cls, id: str, title: str="title", belong_to: Any=None):
        c = cls(id=id, type="title", title=[])
        c.set_text(title)
        return c

class RichText(BasePageProperty):
    type: Literal["rich_text"]
    rich_text: list[RichTextUnion]

    def get_value(self):
        return "".join([i.plain_text for i in super().get_value()])

    def set_text(self, text: str):
        if isinstance(text, str):
            self.rich_text = [Text.new(text)]
        elif isinstance(text, RichTextUnion):
            self.rich_text = [text]
        else:
            raise TypeError(
                "text should be one of str, Text, MentionText, EquationText.")
        self.is_modified = True

    @classmethod
    def new(cls, id: str, text: str="", belong_to: Any=None):
        c = cls(id=id, type="rich_text", rich_text=[], belong_to=belong_to)
        if text:
            c.set_text(text)
        return c

class Relation(BasePageProperty):
    type: Literal["relation"]
    has_more: bool = Field(exclude=True)
    # page relation object that contain id of page
    relation: list[NotionObjectModel]
    is_paginated: bool = True

    async def get_paginated_items(self):
        if not self.has_more:
            return
        from .cache import cache
        client = cache.client
        self.relation = []
        start_cursor = {}
        has_more = 1
        while has_more:
            r = await client.pages.properties.retrieve(page_id=self.parent.id, property_id=self.id, **start_cursor)
            for i in r["results"]:
                self.relation.append(NotionObjectModel(**i["relation"]))
            has_more = r["has_more"]
            if has_more:
                start_cursor = query_finder(r["next_url"])
        return self

    @staticmethod
    def get_notion_object(obj):
        if isinstance(obj, Page):
            return NotionObjectModel(id=obj.id)
        elif isinstance(obj, str):
            return NotionObjectModel(id=obj)
        else:
            raise TypeError("page shhould be one of str, Page")

    def add_page(self, page: Page | str = None):
        from .cache import cache
        page = self.get_notion_object(page)
        parent_db = cache.databases.get(self.belong_to.relation.database_id)
        if parent_db and page in [NotionObjectModel(p.id) for p in parent_db.pages.values()]:
            self.relation.append(page)
        self.is_modified = True
        return self

    def delete_page(self, page: Page | str = None):
        try:
            self.relation.remove(self.get_notion_object(page))
            self.is_modified = True
        except ValueError:
            pass
        return self

    def clear_pages(self):
        self.relation = []
        self.is_modified = True
        return self

    def add_pages(self, pages: list[Page | str]):
        for i in pages:
            try:
                self.add_page(i)
            except TypeError:
                pass
        return self

    @classmethod
    def new(cls, id: str, pages: list[Page | str]=[], belong_to: Any=None):
        c = cls(id=id, type="relation", relation=[], has_more=False, belong_to=belong_to)
        if pages:
            c.add_pages(pages)
        return c

class RollupArray(ArrayTypeObject):
    function: RollupFunctionType


class Rollup(BasePageProperty):
    type: Literal["rollup"]
    rollup: RollupArray
    editable: bool = False


class Checkbox(BasePageProperty):
    type: Literal["checkbox"]
    checkbox: bool

    @classmethod
    def new(cls, id: str, check: bool=False, belong_to: Any=None):
        return cls(id=id, type="checkbox", checkbox=check, belong_to=belong_to)


class Date(BasePageProperty):
    type: Literal["date"]
    date: DateObject | None

    @property
    def start(self):
        return self.date.start

    @property
    def end(self):
        return self.date.end

    @property
    def time_zone(self):
        return self.date.time_zone

    @start.setter
    def start(self, v):
        if self.date is None:
            self.date = DateObject.new(start=v)
        else:
            self.date.start = v
        self.is_modified = True

    @end.setter
    def end(self, v):
        if self.date is None:
            raise ValueError("please specify start time first")
        else:
            self.date.end = v
        self.is_modified = True

    @time_zone.setter
    def time_zone(self, v):
        if self.date is None:
            raise ValueError("please specify start time first")
        else:
            self.date.time_zone = v
        self.is_modified = True

    def reschedule(self, td):
        if not isinstance(td, timedelta):
            raise TypeError("argument should be type of datetime.timedelta")
        self.start = self.start+td
        self.end = self.end+td
        self.is_modified = True
    
    @classmethod
    def new(cls, 
            id: str, 
            start: dt | None=None, 
            end: dt | None=None, 
            time_zone: str | None=None,
            belong_to: Any=None
            ):
        c = cls(id=id, type="date", date=None, belong_to=belong_to)
        if start is not None:
            c.start=start
            c.end=end
            c.time_zone=time_zone
        return c


class Email(BasePageProperty):
    type: Literal["email"]
    email: EmailStr | None

    @classmethod
    def new(cls, id: str, email: str=None, belong_to: Any=None):
        c = cls(id=id, type="email", email=email, belong_to=belong_to)
        if email:
            c.email = email
        return c


class Files(BasePageProperty):
    type: Literal["files"]
    files: list[File]

    def add_file(self, url: str):
        if len(urlparse(url).scheme):
            self.url = ExternalFile.new(url=url)
        else:
            raise ValueError(
                "Provided string is not valid url")
    
    @classmethod
    def new(cls, id: str, file: str=None, belong_to: Any=None):
        c = cls(id=id, type="files", files=[], belong_to=belong_to)
        if file:
            c.add_file(file)
        return c

class Formula(BasePageProperty):
    """ uneditable """
    type: Literal["formula"]
    formula: FormulaValues
    editable: bool = False


class Number(BasePageProperty):
    type: Literal["number"]
    number: int | float | None

    @classmethod
    def new(cls, id: str, number: int | float | None=None, belong_to: Any=None):
        return cls(id=id, type="number", number=number, belong_to=belong_to)


class People(BasePageProperty):
    type: Literal["people"]
    people: list[User]

    @classmethod
    def new(cls, id: str, people: list[User]=[], belong_to: Any=None):
        return cls(id=id, type="people", people=[], belong_to=belong_to)


class PhoneNumber(BasePageProperty):
    type: Literal["phone_number"]
    phone_number: str | None

    @classmethod
    def new(cls, id: str, phone_number: str=None, belong_to: Any=None):
        return cls(id=id, type="phone_number", phone_number=phone_number, belong_to=belong_to)
    
class Url(BasePageProperty):
    type: Literal["url"]
    url: HttpUrl | None

    def get_value(self):
        return str(super().get_value())
    
    @classmethod
    def new(cls, id:str, url: str = None, belong_to: Any=None):
        return cls(id=id, type="url", url=url, belong_to=belong_to)


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

name_class_link = {
    "checkbox": Checkbox,
    "created_by": CreatedBy,
    "created_time": CreatedTime,
    "date": Date,
    "email": Email,
    "files": Files,
    "formula": Formula,
    "last_edited_by": LastEditedBy,
    "last_edited_time": LastEditedTime,
    "multi_select": MultiSelect,
    "number": Number,
    "people": People,
    "phone_number": PhoneNumber,
    "relation": Relation,
    "rollup": Rollup,
    "rich_text": RichText,
    "select": Select,
    "status": Status,
    "title": Title,
    "url": Url,
}