"""
Emoji objects

https://developers.notion.com/reference/emoji-object
"""

from .base_model import NotionBaseModel
from typing import Literal
from emoji import UNICODE_EMOJI

class Emoji(NotionBaseModel):
    type: Literal["emoji"]
    emoji: str

    @classmethod
    def new(cls, emoji: str):
        if emoji not in UNICODE_EMOJI:
            raise ValueError(emoji + " is not emoji.")
        return cls(type="emoji", emoji=emoji)
