from pydantic import BaseModel, model_serializer
from pydantic import UUID4, AnyUrl
from datetime import datetime
from enum import Enum
from uuid import UUID

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
    rescursive pydantic.BaseModel decoder for all possible objects(types) in Notion API.
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


class NotionBaseModel(BaseModel, validate_assignment=True):
    """
    Model for object that not has id in fields
    """
    @model_serializer
    def model_serialize(self):
        return {i: json_decoder(self.__getattribute__(i)) for i in self.model_fields_set}


class NotionObjectModel(NotionBaseModel):
    """
    Model for object instance that has id in fields
    """
    id: UUID4




