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

    @classmethod
    def new(cls, database_id: str):
        return cls(type="database_id", database_id=database_id)

class PageParent(NotionBaseModel):
    type: Literal["page_id"]
    page_id: str

    @classmethod
    def new(cls, page_id:str):
        return cls(type="page_id", page_id=page_id)
    
class WorkspaceParent(NotionBaseModel):
    type: Literal["workspace"]
    workspace: bool

    @classmethod
    def new(cls, workspace: bool):
        return cls(type="workspace", workspace=workspace)
    
class BlockParent(NotionBaseModel):
    type: Literal["block_id"]
    block_id: str

    @classmethod
    def new(cls, block_id: str):
        return cls(type="block_id", block_id=block_id)
    
Parent = Union[
    DatabaseParent,
    PageParent,
    WorkspaceParent,
    BlockParent,
]