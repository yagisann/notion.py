from .base_builder import *
from .helper import SelectOptionsBuilder, RollupConfig
from ..models.database_property import *
from ..models.base_object import StatusOptions, SelectOptionList

from typing import Any

class BaseDbPropertyBuilder(BaseBuilder):
    __doc__ = """
Argument:
    rename: Specify arbitrary str if rename the property. if not, specify None.
    remove: Specify True if remove the property. if not, specify False
    """
    def __init__(self, rename: None | str=None, remove: bool=False, **kw):
        super().__init__(**kw)
        self.rename = rename
        self._remove = False
        self.remove = remove
    
    @property
    def remove(self):
        return self._remove
    
    @remove.setter
    def remove(self, value):
        if (self.name == "title") and (value):
            raise ValueError("Title cannot be removed")
        self._remove = value
    
    def build(self):
        if self.remove:
            return None
        payload = {self.name: self.get_payload()}
        if self.rename:
            payload["name"] = self.rename
        return payload
    
    def get_payload(self):
        return {}

class CreatedByColumn(BaseDbPropertyBuilder):
    name = "created_by"

class CreatedTimeColumn(BaseDbPropertyBuilder):
    name = "created_time"

class LastEditedByColumn(BaseDbPropertyBuilder):
    name = "last_edited_by"

class LastEditedTimeColumn(BaseDbPropertyBuilder):
    name = "last_edited_time"

class MultiSelectColumn(BaseDbPropertyBuilder):
    fields_setting = {
        "multi_select": {
            list: lambda x: SelectOptionsBuilder(x),
            SelectOptionsBuilder: lambda x: x,
            SelectOptionList: lambda x: SelectOptionsBuilder(x.options),
        }
    }
    name = "multi_select"

    def get_payload(self):
        return {"options": self.fields_value["multi_select"].build()}

class SelectColumn(BaseDbPropertyBuilder):
    fields_setting = {
        "select": {
            list: lambda x: SelectOptionsBuilder(x),
            SelectOptionsBuilder: lambda x: x,
            SelectOptionList: lambda x: SelectOptionsBuilder(x.options),
        }
    }
    name = "select"

    def get_payload(self):
        return {"options": self.fields_value["select"].build()}

class StatusColumn(BaseDbPropertyBuilder):
    """Status is not possible to update via the API."""
    fields_setting = {
        "status": {
            dict: lambda x: x,
            StatusOptions: lambda x: x.model_dump()
        }
    }
    name = "status"
    
    def get_payload(self):
        return {}

class TitleColumn(BaseDbPropertyBuilder):
    name = "title"

class RichTextColumn(BaseDbPropertyBuilder):
    name = "rich_text"

class RelationColumn(BaseDbPropertyBuilder):
    fields_setting = {
        "relation": {
            str: lambda x: SingleRelationConfig(database_id=x, type="single_property", single_property={}),
            SingleRelationConfig: lambda x: x,
            DualRelationConfig: lambda x: x,
        }
    }
    name = "relation"

    def get_payload(self):
        return self.fields_value["relation"].model_dump()

class RollupColumn(BaseDbPropertyBuilder):
    fields_setting = {
        "rollup": {
            dict: lambda x: RollupConfig(x),
            RollupConfig: lambda x: x,
        }
    }
    name = "rollup"

    def get_payload(self):
        return self.fields_value["rollup"].model_dump()

class CheckboxColumn(BaseDbPropertyBuilder):
    name = "checkbox"

class DateColumn(BaseDbPropertyBuilder):
    name = "date"

class EmailColumn(BaseDbPropertyBuilder):
    name = "email"

class FilesColumn(BaseDbPropertyBuilder):
    name = "files"

class FormulaColumn(BaseDbPropertyBuilder):
    fields_setting = {
        "formula": {
            str: lambda x: FormulaConfig(expression=x),
            FormulaConfig: lambda x: x,
        }
    }
    name = "formula"

    def get_payload(self):
        return self.fields_value["formula"].model_dump()

class NumberColumn(BaseDbPropertyBuilder):
    fields_setting = {
        "number": {
            str: lambda x: NumberConfig(format=x),
            NumberFormatType: lambda x: NumberConfig(format=x),
            NumberConfig: lambda x: x,
        }
    }
    default_value = {
        "number": NumberConfig(format="number")
    }
    name = "number"

    def get_payload(self):
        return self.fields_value["number"].model_dump()

class PeopleColumn(BaseDbPropertyBuilder):
    name = "people"

class PhoneNumberColumn(BaseDbPropertyBuilder):
    name = "phone_number"

class UrlColumn(BaseDbPropertyBuilder):
    name = "url"


class DbColumnsBuilder:
    def __init__(self, columns: dict[str, Any]):
        self.add_queue = columns
        self.columns = dict()
        self._exec_add()

    def add_columns(self, columns: dict[str, Any]):
        self.add_queue.update(**columns)
        self._exec_add()

    def _exec_add(self):
        for name, column in self.add_queue.items():
            self.validate(name, column)
            self.columns[name] = column

    def validate(self, name, column):
        if not isinstance(name, str):
            raise TypeError(f"Column name should be type of str, not '{type(name)}'")
        if not issubclass(type(column), BaseDbPropertyBuilder):
            raise TypeError(f"Column should be a type of BaseDbPropertyBuilder, not '{type(column)}'")
        if isinstance(column, RollupColumn):
            if not any([isinstance(i, RelationColumn) for i in {**self.add_queue, **self.columns}.values()]):
                raise TypeError(f"To add RollupColummn, RelationColumn should be added")
    
    def __bool__(self):
        return self.columns != dict()
    
    def build(self):
        if not any([isinstance(column, TitleColumn) for column in self.columns.values()]):
            raise ValueError("Database properties must contain title column.\nTo add column, use DatabasePropertyBuilder.add_fields method.")
        return {name: column.build() for name, column in self.columns.items()}

class_link = {
    Checkbox: CheckboxColumn,
    CreatedBy: CreatedByColumn,
    CreatedTime: CreatedTimeColumn,
    Date: DateColumn,
    Email: EmailColumn,
    Files: FilesColumn,
    Formula: FormulaColumn,
    LastEditedBy: LastEditedByColumn,
    LastEditedTime: LastEditedTimeColumn,
    MultiSelect: MultiSelectColumn,
    Number: NumberColumn,
    People: PeopleColumn,
    PhoneNumber: PhoneNumberColumn,
    Relation: RelationColumn,
    Rollup: RollupColumn,
    RichText: RichTextColumn,
    Select: SelectColumn,
    Status: StatusColumn,
    Title: TitleColumn,
    Url: UrlColumn,
}

def transform_scheme_object(i):
    if isinstance(i, (MultiSelect, Select, Status, Relation, Rollup, Formula, Number)):
        return class_link[type(i)](**{i.type: i.__getattribute__(i.type)})
    else:
        return class_link[type(i)]()

class DatabasePropertyBuilder(BaseBuilder):
    __doc__ = """
Usage example:

Build properties (from empty)
```py
import notion
from notion.builder import *

project_options = SelectOptionsBuilder([
    "Proj-x",
    OptionBuilder(name="Proj-Lemon", color="yellow"),
    OptionBuilder(name="Proj-Apple", color="red"),
    OptionBuilder(name="Proj-Melon", color="green"),
])

columns = {
    "task name": TitleColumn(),
    "project": MultiSelectColumn(multi_select=project_options)
    "assigned": PeopleColumn(),
    "until": DateColumn(),
}

property_builder = DatabasePropertyBuilder(columns=columns)


client = notion.Client(token="your token here")
await client.create_database(
    builder=MyDatabaseBuilder(title="Projects Overview", description="summation of tasks."),
    properties=property_builder,
    parent=PageParentBuilder(page_id="e256186b-f566-4e3c-9bb7-bf7f0d4ac20a")
)
```


Modify properties (from existing database)
```py
import notion
from notion.builder import DatabaseBuilder, DatabasePropertyBuilder

client = notion.Client(token="your token here")
database = await client.fetch_database("42740044-ebe2-432a-8206-d806bfd41689")

property_builder = DatabasePropertyBuilder(model_db=database.properties)
property_builder.add_columns({
    "last edit": LastEditedBy
})
property_builder["assingned"].remove = True
property_builder["project"].rename = "parent"

await database.edit(properties=property_builder)
```
"""
    fields_setting = {
        "columns": {
            dict: lambda x: DbColumnsBuilder(x),
            DbColumnsBuilder: lambda x: x,
        },
        "model_db": {
            dict: lambda x: DbColumnsBuilder({name: transform_scheme_object(model) for name, model in x.items()})
        }
    }

    def _form_data(self, kwargs: dict, initialize: bool=True, ignore_extra=False):
        super()._form_data(kwargs=kwargs, initialize=initialize, ignore_extra=ignore_extra)
        if isinstance(self.fields_value["columns"], FieldUndefined):
            self.fields_value["columns"] = self.fields_value["model_db"]
        if isinstance(self.fields_value["columns"], FieldUndefined):
            raise ValueError("One of columns, model_db argument must be provided.")
        return self
    
    def add_columns(self, columns: dict):
        self.fields_value["columns"].add_columns(columns)
    
    def __getitem__(self, key):
        return self.fields_value["columns"].columns[key]
    
    def build(self):
        return self.fields_value["columns"].build()
    