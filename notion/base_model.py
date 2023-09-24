from __future__ import annotations
from typing import TYPE_CHECKING

from pydantic import BaseModel, model_serializer, ConfigDict
from pydantic import UUID4, AnyUrl
from datetime import datetime
from enum import Enum
from uuid import UUID


if TYPE_CHECKING:
    from notion_client import AsyncClient

__all__ = (
    "NotionBaseModel",
    "NotionObjectModel",
)

type_conversion = {
    Enum: lambda x: x.value,
    datetime: lambda x: x.isoformat().replace("+00:00", "Z"),
    UUID: lambda x: str(x),
    AnyUrl: lambda x: str(x),
}

def json_decoder(obj):
    """
    rescursive pydantic.BaseModel decoder for all available objects(types) in Notion API.
    """
    if obj is None:
        return obj
    if isinstance(obj, (bool, int, float, complex, str)):
        return obj
    if issubclass(type(obj), NotionBaseModel):
        return obj.model_dump()
    if isinstance(obj, list):
        return [json_decoder(i) for i in obj]
    if isinstance(obj, dict):
        return {i: json_decoder(j) for i, j in obj.items()}

    for i, j in type_conversion.items():
        if issubclass(type(obj), i):
            return j(obj)
    return obj

class NotionBaseModel(BaseModel):
    """
    Custamized base model for this module
    """
    model_config = ConfigDict(validate_assignment=True)

    @model_serializer(mode="wrap")
    def model_serialize(self, _handler, _info) -> dict:
        if _info.include is not None:
            return {i: json_decoder(self.__getattribute__(i)) for i in _info.include}
        exclude = [] if _info.exclude is None else _info.exclude
        exclude += [f for f, i in self.model_fields.items() if i.exclude==True]
        return {i: json_decoder(self.__getattribute__(i)) for i in self.model_fields_set if i not in exclude}


class NotionObjectModel(NotionBaseModel):
    """
    Model for object instance that has id in fields
    """
    id: UUID4
