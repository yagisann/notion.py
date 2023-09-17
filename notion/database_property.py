"""
Database property objects

https://developers.notion.com/reference/property-object
https://developers.notion.com/reference/property-schema-object
"""
from __future__ import annotations
from pydantic import field_validator, UUID4, Field
from .base_model import NotionBaseModel
from .enums import Color
from .general_object import EmptyObject, SelectOptionList, StatusOptions
from typing import Literal, Union, Any
from enum import Enum


class SingleRelationConfig(NotionBaseModel):
    database_id: UUID4
    type: Literal["single_property"]
    single_property: EmptyObject

    def switch(self):
        return DualRelationConfig(
            database_id=self.database_id,
            type="dual_property",
            dual_property={}
        )

    def build(self):
        return self.model_dump()


class DualProperty(NotionBaseModel):
    """ cannot update directly via API """
    synced_property_name: str
    synced_property_id: str


class DualRelationConfig(NotionBaseModel):
    database_id: UUID4
    type: Literal["dual_property"]
    dual_property: DualProperty | EmptyObject

    def switch(self):
        return SingleRelationConfig(
            database_id=self.database_id,
            type="single_property",
            single_property={}
        )

    def build(self):
        return {**self.model_dump(exclude={"dual_property"}), **{"dual_property": {}}}


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
    rename: None | str = Field(default=None, min_length=1)
    remove: bool = False

    @field_validator("remove")
    @classmethod
    def remove_validate(cls, value):
        if (cls.name == "title") and (value):
            raise ValueError("Title cannot be removed")
        return value

    def build(self):
        if self.remove:
            return None
        payload = {self.name: self.get_payload()}
        if self.rename:
            payload["name"] = self.rename
        return payload

    def get_payload(self):
        return self.__getattribute__(self.type).model_dump()

    @classmethod
    def new(cls, name: str = ""):
        return cls(**cls._new.default, id="", name=name)


class CreatedBy(BaseDbProperty):
    type: Literal["created_by"]
    created_by: EmptyObject
    _new: Any = {
        "type": "created_by",
        "created_by": {},
    }


class CreatedTime(BaseDbProperty):
    type: Literal["created_time"]
    created_time: EmptyObject
    _new: Any = {
        "type": "created_time",
        "created_time": {},
    }


class LastEditedBy(BaseDbProperty):
    type: Literal["last_edited_by"]
    last_edited_by: EmptyObject
    _new: Any = {
        "type": "last_edited_by",
        "last_edited_by": {},
    }


class LastEditedTime(BaseDbProperty):
    type: Literal["last_edited_time"]
    last_edited_time: EmptyObject
    _new: Any = {
        "type": "last_edited_time",
        "last_edited_time": {},
    }


class MultiSelect(BaseDbProperty):
    type: Literal["multi_select"]
    multi_select: SelectOptionList
    _new: Any = {
        "type": "multi_select",
        "multi_select": SelectOptionList.new(),
    }

    def get_option(self, name: str):
        return self.multi_select.get(name)

    def add_option(self, name: str, color: Color = None):
        self.multi_select.append(name, color)
        return self

    def delete_option(self, name: str):
        self.multi_select.delete(name)
        return self

    def get_payload(self):
        return self.multi_select.build()


class Select(BaseDbProperty):
    type: Literal["select"]
    select: SelectOptionList
    _new: Any = {
        "type": "select",
        "select": SelectOptionList.new(),
    }

    def get_option(self, name: str):
        return self.select.get(name)

    def add_option(self, name: str, color: Color = None):
        self.select.append(name, color)
        return self

    def delete_option(self, name: str):
        self.select.delete(name)
        return self

    def get_payload(self):
        return self.select.build()


class Status(BaseDbProperty):
    type: Literal["status"]
    status: StatusOptions
    _new: Any = {
        "type": "status",
        "status": StatusOptions.new(),
    }

    def get_payload(self):
        """ Status updates via API are currently not supported. """
        return {}


class Title(BaseDbProperty):
    type: Literal["title"]
    title: EmptyObject
    _new: Any = {
        "type": "title",
        "title": {}
    }


class RichText(BaseDbProperty):
    type: Literal["rich_text"]
    rich_text: EmptyObject
    _new: Any = {
        "type": "rich_text",
        "rich_text": {}
    }


class Relation(BaseDbProperty):
    type: Literal["relation"]
    relation: SingleRelationConfig | DualRelationConfig

    def set_database(self, database_id: str):
        self.relation.database_id = database_id
        return self

    def set_type(self, type: str):
        if type not in ["single_property", "dual_property"]:
            raise ValueError(
                "Relation type should be one of 'single_property' or 'dual_property'.")
        self.relation = self.relation.switch()
        return self

    @classmethod
    def new(cls, database_id: str, type: str = "single_property", name: str = ""):
        if type not in ["single_property", "dual_property"]:
            raise ValueError(
                "Relation type should be one of 'single_property' or 'dual_property'.")
        if type == "single_property":
            rel = SingleRelationConfig(
                database_id=database_id, type=type, single_property={})
        else:
            rel = DualRelationConfig(
                database_id=database_id, type=type, dual_property={})
        return cls(type="relation", relation=rel, id="", name=name)


class Rollup(BaseDbProperty):
    type: Literal["rollup"]
    rollup: RollupConfig

    def set_function(self, fn_type: str | RollupFunctionType):
        self.rollup.function = fn_type
        return self

    def set_relation(self, relation: Relation = None, name: str = None, id: str = None):
        if not (relation or (name and id)):
            raise ValueError("relation or name/id pair must be provided.")
        if relation:
            self.rollup.relation_property_name = relation.name
            self.rollup.relation_property_id = relation.id
        else:
            self.rollup.relation_property_name = name
            self.rollup.relation_property_id = id
        return self

    def set_rollup_item(self, rollup_property: BaseDbProperty = None, name: str = None, id: str = None):
        if not (rollup_property or (name and id)):
            raise ValueError(
                "rollup_property or name/id pair must be provided.")
        if rollup_property:
            self.rollup.rollup_property_name = rollup_property.name
            self.rollup.rollup_property_id = rollup_property.id
        else:
            self.rollup.rollup_property_name = name
            self.rollup.rollup_property_id = id
        return self

    @classmethod
    def new(cls, relation: Relation, rollup_property: BaseDbProperty, fn_type: str | RollupFunctionType = RollupFunctionType.show_original):
        return cls(
            type="rollup",
            rollup=RollupConfig(
                function=fn_type,
                relation_property_id=relation.id,
                relation_property_name=relation.name,
                rollup_property_id=rollup_property.id,
                rollup_property_name=rollup_property.name,
            )
        )


class Checkbox(BaseDbProperty):
    type: Literal["checkbox"]
    checkbox: EmptyObject
    _new: Any = {
        "type": "checkbox",
        "checkbox": {},
    }


class Date(BaseDbProperty):
    type: Literal["date"]
    date: EmptyObject
    _new: Any = {
        "type": "date",
        "date": {},
    }


class Email(BaseDbProperty):
    type: Literal["email"]
    email: EmptyObject
    _new: Any = {
        "type": "email",
        "email": {},
    }


class Files(BaseDbProperty):
    type: Literal["files"]
    files: EmptyObject
    _new: Any = {
        "type": "files",
        "files": {},
    }


class Formula(BaseDbProperty):
    type: Literal["formula"]
    formula: FormulaConfig
    _new: Any = {
        "type": "formula",
        "formula": FormulaConfig(expression=""),
    }

    def set_formula(self, expression: str):
        self.formula.expression = expression
        return self

    @classmethod
    def new(cls, expression: str = ""):
        return super().new().set_formula(expression)


class Number(BaseDbProperty):
    type: Literal["number"]
    number: NumberConfig
    _new: Any = {
        "type": "number",
        "number": NumberConfig(format="number"),
    }

    def set_format(self, format: str | NumberFormatType):
        self.number.format = format
        return self

    @classmethod
    def new(cls, format: str | NumberFormatType = "number"):
        return super().new().set_formula(format)


class People(BaseDbProperty):
    type: Literal["people"]
    people: EmptyObject
    _new: Any = {
        "type": "people",
        "people": {},
    }


class PhoneNumber(BaseDbProperty):
    type: Literal["phone_number"]
    phone_number: EmptyObject
    _new: Any = {
        "type": "phone_number",
        "phone_number": {},
    }


class Url(BaseDbProperty):
    type: Literal["url"]
    url: EmptyObject
    _new: Any = {
        "type": "url",
        "url": {},
    }


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
