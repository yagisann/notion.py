"""
File objects

https://developers.notion.com/reference/file-object
"""

from .base_model import NotionBaseModel
from .general_object import UrlObject
from typing import Literal, Union
from datetime import datetime as dt

__all__ = (
    "NotionHostedFile",
    "ExternalFile",
    "File",
)

class FileProperty(UrlObject):
    expiry_time: dt

class NotionHostedFile(NotionBaseModel):
    type: Literal["file"]
    file: FileProperty

class ExternalFile(NotionBaseModel):
    type: Literal["external"]
    external: UrlObject

    @classmethod
    def new(cls, url: str):
        return cls(type="external", external={"url": url})


File = Union[
    NotionHostedFile,
    ExternalFile,
]