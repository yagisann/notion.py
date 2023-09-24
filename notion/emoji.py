"""
Emoji objects

https://developers.notion.com/reference/emoji-object
"""

from .base_model import NotionBaseModel
from typing import Literal
import emoji as em

class Emoji(NotionBaseModel):
    type: Literal["emoji"]
    emoji: str

    @classmethod
    def new(cls, emoji: str):
        if not em.is_emoji(emoji):
            raise ValueError(emoji + " is not emoji.")
        return cls(type="emoji", emoji=emoji)
