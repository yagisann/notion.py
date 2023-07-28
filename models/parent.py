"""
Parent objects

https://developers.notion.com/reference/parent-object
"""

from .base_model import NotionBaseModel
from typing import Literal, Union

__all__ = (
    "DatabaseParent",
    "PageParent",
    "WorkspaceParent",
    "BlockParent",
    "Parent",
)

class DatabaseParent(NotionBaseModel):
    type: Literal["database_id"]
    database_id: str

class PageParent(NotionBaseModel):
    type: Literal["page_id"]
    page_id: str

class WorkspaceParent(NotionBaseModel):
    type: Literal["workspace"]
    workspace: bool

class BlockParent(NotionBaseModel):
    type: Literal["block_id"]
    block_id: str

Parent = Union[
    DatabaseParent,
    PageParent,
    WorkspaceParent,
    BlockParent,
]