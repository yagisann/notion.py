"""
Comment objects

https://developers.notion.com/reference/comment-object
"""

from pydantic import UUID4
from .base_model import NotionObjectModel, NotionBaseModel
from .rich_text import RichText
from .user import User
from .parent import Parent
from typing import Literal
from datetime import datetime as dt

__all__ = (
    "Comment",
)

class Comment(NotionObjectModel):
    type: Literal["comment"]
    parent: Parent
    discussion_id: UUID4
    created_time: dt
    last_edited_time: dt
    created_by: User
    rich_text: list[RichText]
