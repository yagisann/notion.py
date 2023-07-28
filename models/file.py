"""
File objects

https://developers.notion.com/reference/file-object
"""

from pydantic import HttpUrl
from .base_model import NotionBaseModel
from .base_object import UrlObject
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


File = Union[
    NotionHostedFile,
    ExternalFile,
]