from .base_builder import *
from .exceptions import *
from .helper import SelectOptionsBuilder, OptionBuilder, text_parser, files_parser, people_list_parser, url_detector, nothing

from ..models.base_object import StatusOptions, SelectOptionList, SelectOption, DateObject. EmailObject
from ..models.base_model import NotionObjectModel
from ..models.file import ExternalFile
from ..models.page_property import (
    Checkbox as CheckboxModel
    CreatedBy as CreatedByModel
    CreatedTime as CreatedTimeModel
    Date as DateModel
    Email as EmailModel
    Files as FilesModel
    Formula as FormulaModel
    LastEditedBy as LastEditedByModel
    LastEditedTime as LastEditedTimeModel
    MultiSelect as MultiSelectModel
    Number as NumberModel
    People as PeopleModel
    PhoneNumber as PhoneNumberModel
    Relation as RelationModel
    Rollup as RollupModel
    RichText as RichTextModel
    Select as SelectModel
    Status as StatusModel
    Title as TitleModel
    Url as UrlModel
)

from datetime import datetime as dt
from typing import Any


class BasePagePropertyBuilder(BaseBuilder):
    def __init__(self, arg=None, **kw):
        if arg is not None:
            kw[self.name] = arg
        super().__init__(**kw)
    
    def build(self):
        if not self.updatable:
            raise BuilderExeption(f"{self.name} property is not updatable.")
        return {self.name: self.get_payload()}

class CreatedBy(BasePagePropertyBuilder):
    fields_setting = {CreatedByModel: nothing}
    name = "created_by"
    updatable = False

class CreatedTime(BasePagePropertyBuilder):
    fields_setting = {CreatedTimeModel: nothing}
    name = "created_time"
    updatable = False

class LastEditedBy(BasePagePropertyBuilder):
    fields_setting = {LastEditedByModel: nothing}
    name = "last_edited_by"
    updatable = False

class LastEditedTime(BasePagePropertyBuilder):
    fields_setting = {LastEditedTimeModel: nothing}
    name = "last_edited_time"
    updatable = False

class MultiSelect(BasePagePropertyBuilder):
    fields_setting = {
        "multi_select": {
            list: lambda x: SelectOptionsBuilder(x),
            SelectOptionsBuilder: nothing,
            SelectOptionList: lambda x: SelectOptionsBuilder(x.options),
            MultiSelectModel: lambda x: SelectOptionsBuilder(x.multi_select.options),
        },
    }
    name = "multi_select"
    updatable = True

    def get_payload(self):
        return {"options": self.fields_value["multi_select"].build(include_color=False)}

class Select(BasePagePropertyBuilder):
    fields_setting = {
        "select": {
            str: lambda OptionBuilder(x),
            OptionBuilder: nothing,
            SelectOption: lambda x: OptionBuilder(x.name),
            SelectModel: lambda x: OptionBuilder(x.select.name), 
        }
    }
    name = "select"
    updatable = True

    def get_payload(self):
        return {"options": self.fields_value["select"].build(include_color=False)}

class Status(BasePagePropertyBuilder):
    fields_setting = {
        "status": {
            str: lambda OptionBuilder(x),
            OptionBuilder: nothing,
            SelectOption: lambda x: OptionBuilder(x.name),
            StatusModel: lambda x: OptionBuilder(x.status.name), 
        }
    }
    name = "status"
    updatable = True
    
    def get_payload(self):
        return self.fields_value["status"].build(include_color=Fale)

class Title(BasePagePropertyBuilder):
    fields_setting = {
        "title": {**text_parser, **{TitleModel: lambda x: x.model_dump()["title"]}},
    }
    name = "title"
    updatable = True

    def get_payload(self):
        return self.fields_value["title"]

class RichText(BasePagePropertyBuilder):
    fields_setting = {
        "rich_text": {**text_parser, **{RichTextModel: lambda x: x.model_dump()["rich_text"]}},
    }
    name = "rich_text"
    updatable = True

    def get_payload(self):
        return self.fields_value["rich_text"]

class Relation(BasePagePropertyBuilder):
    fields_setting = {
        "relation": {
            str: lambda x: [NotionObjectModel(id=x)],
            list: lambda x: [NotionObjectModel(id=i) for i in x],
            RelationModel: lambda x: x.relation,
        }
    }
    name = "relation"
    updatable = True

    def get_payload(self):
        return [i.model_dump() for i in self.fields_value["relation"]]

class Rollup(BasePagePropertyBuilder):
    fields_setting = {RollUpModel: nothing}
    name = "rollup"
    updatable = False

class Checkbox(BasePagePropertyBuilder):
    fields_setting = {
        "checkbox": {
            bool: nothing,
            CheckboxModel: lambda x: x.checkbox,
        }
    }
    name = "checkbox"
    updatable=True

    def get_payload(self):
        return self.fields_value["checkbox"]

class Date(BasePagePropertyBuilder):
    fields_setting = {
        "date": {
            dt: lambda x: DateObject(start=x),
            DateObject: nothing,
            DateModel: lambda x: x.date,
        }
    }
    name = "date"
    updatable = True

    def get_payload(self):
        return self.fields_value["date"].model_dump()

class Email(BasePagePropertyBuilder):
    fields_setting = {
        "email": {
            str: lambda x: EmailObject(email=x),
            EmailObject: nothing,
            EmailModel: lambda x: x.email,
        }
    }
    name = "email"
    updatable = True

    def get_payload(self):
        return self.fields_value["email"].model_dump()

class Files(BasePagePropertyBuilder):
    fields_setting = {
        "files": {**files_parser, **{FilesModel: lambda x: x.files}}
    }
    name = "files"
    updatable = True

    def get_payload(self):
        return [i.model_dump() for i in self.fields_value["files"]]

class Formula(BasePagePropertyBuilder):
    fields_setting = {
        "formula": {FormulaModel: nothing}
    }
    name = "formula"
    updatable = False

class Number(BasePagePropertyBuilder):
    fields_setting = {
        "number": {
            int: nothing,
            float: nothing,
            NumberModel: lambda x: x.number,
        }
    }
    name = "number"
    updatable = True

    def get_payload(self):
        return self.fields_value["number"]

class People(BasePagePropertyBuilder):
    fields_setting = {
        "people": {
            str: lambda x: PeopleModel(type="people", people=[{"object": "user", "id": x}]),
            list: lambda x: people_list_parser(x),
            PeopleModel: nothing,
        }
    }
    name = "people"
    updatable = True

    def get_payload(self):
        return [i.model_dump() for i in self.fields_value["people"]]

class PhoneNumber(BasePagePropertyBuilder):
    fields_setting = {
        "phone_number": {
            str: nothing,
            PhoneNumberModel: lambda x: x.phone_number
        }
    }
    name = "phone_number"
    updatable = True

    def get_payload(self):
        return self.fields_value["phone_number"]

class Url(BasePagePropertyBuilder):
    fields_setting = {
        "url": {
            str: lambda x: url_detector(x),
            UrlModel: lambda x: str(x.url)
        }
    }
    name = "url"
    updatable = True

    def get_payload(self):
        return self.fields_value["url"]


class_link = {
    CheckboxModel: Checkbox
    CreatedByModel: CreatedBy
    CreatedTimeModel: CreatedTime
    DateModel: Date
    EmailModel: Email
    FilesModel: Files
    FormulaModel: Formula
    LastEditedByModel: LastEditedBy
    LastEditedTimeModel: LastEditedTime
    MultiSelectModel: MultiSelect
    NumberModel: Number
    PeopleModel: People
    PhoneNumberModel: PhoneNumber
    RelationModel: Relation
    RollupModel: Rollup
    RichTextModel: RichText
    SelectModel: Select
    StatusModel: Status
    TitleModel: Title
    UrlModel: Url
}


class PageValuesBuilder():
    def __init__(self, values: dict[str, Any]):
        self.values = values

    
    def edit_title(self, title_payload):
        for i, j in self.values.items():
            if isinstance(j, Title):
                self.values[i] = Title(TitleModel(title_payload))
                return self
    
    def edit_values(self, new: dict[str, Any]):
        for i, j in new.items():
            if i in self.values:
                if not self.value[i].updatable:
                    raise BuilderExeption(f"{i} is not updatable.")
                if type(j) == type(self.values[i]):
                    self.value[i] = j
                else:
                    try:
                        self.values[i] = self.values[i].__class__(j)
                    except TypeError as e:
                        raise TypeError(f"Error occured while parsing {i} value.\n details: {e}")
            else:
                raise KeyError(f"{i} is not valid name for page property\navailable names: '{', '.join(self.values.keys())}' ")
    
    def build(self):
        return {name: value.build() for name, value in self.values.items() if value.updatable}

class PagePropertyBuilder(BaseBuilder):
    fields_setting = {
        "model_page": {
            dict: lambda x: PageValuesBuilder({name: class_link[type(model)](model) for name. model in x.items()}),
        },
        "title": {**text_parser, **{TitleModel: lambda x: x.model_dump()["title"]}},
        "values": {
            dict: lambda x: PageValuesBuilder(x),
            PageValuesBuilder: nothing,
        },
    }

    def _form_data(self, kwargs: dict, initialize: bool=True, ignore_extra=False):
        super()._form_data(kwargs=kwargs, initialize=initialize, ignore_extra=ignore_extra)
        if isinstance(self.fields_value["values"], FieldUndefined):
            self.fields_value["values"] = self.fields_value["model_page"]
        if isinstance(self.fields_value["values"], FieldUndefined):
            raise ValueError("One of values, model_page argument must be provided.")
        if not isinstance(self.fields_value["title"], FieldUndefined):
            self.fields_value["values"].edit_title(self.fields_value["title"])
        return self
    
    def edit(self, title=None, values=None):
        if title:
            self.set_fields(title=title)
            self.fields_value["values"].edit_title(self.fields_value["title"])
        if values:
            self.fields_value["values"].edit_values(values)
    
    def __getitem__(self, key):
        return self.fields_value["values"].values[key]
    
    def __setitem__(self, key, val):
        self.edit(values={key: val})

    def build(self):
        return self.fields_value["values"].build()