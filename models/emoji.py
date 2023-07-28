"""
Emoji objects

https://developers.notion.com/reference/emoji-object
"""

from .base_model import NotionBaseModel
from typing import Literal

__all__ = (
    "Emoji",
)

class Emoji(NotionBaseModel):
    type: Literal["emoji"]
    emoji: str
