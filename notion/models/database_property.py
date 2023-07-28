"""
Database property objects

https://developers.notion.com/reference/property-object
https://developers.notion.com/reference/property-schema-object
"""
from pydantic import UUID4
from .base_model import NotionBaseModel
from .base_object import EmptyObject, SelectOption, SelectOptionList, OptionGroup, StatusOptions
from typing import Literal, Union
from enum import Enum

class SingleRelationConfig(NotionBaseModel):
    database_id: UUID4
    type: Literal["single_property"]
    single_property: EmptyObject

class DualRelationConfig(NotionBaseModel):
    database_id: UUID4
    type: Literal["dual_property"]
    dual_property: EmptyObject

class RollupFunctionType(Enum):
    average = "average"
    checked = "checked"
    count_per_group = "count_per_group"
    count = "count"
    count_values = "count_values"
    date_range = "date_range"
    earliest_date = "earliest_date"
    empty = "empty"
    latest_date = "latest_date"
    max = "max"
    median = "median"
    min = "min"
    not_empty = "not_empty"
    percent_checked = "percent_checked"
    percent_empty = "percent_empty"
    percent_not_empty = "percent_not_empty"
    percent_per_group = "percent_per_group"
    percent_unchecked = "percent_unchecked"
    range = "range"
    unchecked = "unchecked"
    unique = "unique"
    show_original = "show_original"
    show_unique = "show_unique"
    sum = "sum"

class RollupConfig(NotionBaseModel):
    function: RollupFunctionType
    relation_property_id: str
    relation_property_name: str
    rollup_property_id: str
    rollup_property_name: str

class FormulaConfig(NotionBaseModel):
    expression: str

class NumberFormatType(Enum):
    argentine_peso = "argentine_peso"
    baht = "baht"
    canadian_dollar = "canadian_dollar"
    chilean_peso = "chilean_peso"
    colombian_peso = "colombian_peso"
    danish_krone = "danish_krone"
    dirham = "dirham"
    dollar = "dollar"
    euro = "euro"
    forint = "forint"
    franc = "franc"
    hong_kong_dollar = "hong_kong_dollar"
    koruna = "koruna"
    krona = "krona"
    leu = "leu"
    lira = "lira"
    mexican_peso = "mexican_peso"
    new_taiwan_dollar = "new_taiwan_dollar"
    new_zealand_dollar = "new_zealand_dollar"
    norwegian_krone = "norwegian_krone"
    number = "number"
    number_with_commas = "number_with_commas"
    percent = "percent"
    philippine_peso = "philippine_peso"
    pound = "pound"
    peruvian_sol = "peruvian_sol"
    rand = "rand"
    real = "real"
    ringgit = "ringgit"
    riyal = "riyal"
    ruble = "ruble"
    rupee = "rupee"
    rupiah = "rupiah"
    shekel = "shekel"
    singapore_dollar = "singapore_dollar"
    uruguayan_peso = "uruguayan_peso"
    yen = "yen"
    yuan = "yuan"
    won = "won"
    zloty = "zloty"

class NumberConfig(NotionBaseModel):
    format: NumberFormatType




class BaseDbProperty(NotionBaseModel):
    id: str
    name: str

class CreatedBy(BaseDbProperty):
    type: Literal["created_by"]
    created_by: EmptyObject

class CreatedTime(BaseDbProperty):
    type: Literal["created_time"]
    created_time: EmptyObject

class LastEditedBy(BaseDbProperty):
    type: Literal["last_edited_by"]
    last_edited_by: EmptyObject

class LastEditedTime(BaseDbProperty):
    type: Literal["last_edited_time"]
    last_edited_time: EmptyObject

class MultiSelect(BaseDbProperty):
    type: Literal["multi_select"]
    multi_select: SelectOptionList

class Select(BaseDbProperty):
    type: Literal["select"]
    select: SelectOptionList

class Status(BaseDbProperty):
    type: Literal["status"]
    status: StatusOptions

class Title(BaseDbProperty):
    type: Literal["title"]
    title: EmptyObject

class RichText(BaseDbProperty):
    type: Literal["rich_text"]
    rich_text: EmptyObject

class Relation(BaseDbProperty):
    type: Literal["relation"]
    relation: SingleRelationConfig | DualRelationConfig

class Rollup(BaseDbProperty):
    type: Literal["rollup"]
    rollup: RollupConfig

class Checkbox(BaseDbProperty):
    type: Literal["checkbox"]
    checkbox: EmptyObject

class Date(BaseDbProperty):
    type: Literal["date"]
    date: EmptyObject

class Email(BaseDbProperty):
    type: Literal["email"]
    email: EmptyObject

class Files(BaseDbProperty):
    type: Literal["files"]
    files: EmptyObject

class Formula(BaseDbProperty):
    type: Literal["formula"]
    formula: FormulaConfig

class Number(BaseDbProperty):
    type: Literal["number"]
    number: NumberConfig

class People(BaseDbProperty):
    type: Literal["people"]
    people: EmptyObject

class PhoneNumber(BaseDbProperty):
    type: Literal["phone_number"]
    phone_number: EmptyObject

class Url(BaseDbProperty):
    type: Literal["url"]
    url: EmptyObject


DatabaseProperty = Union[
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