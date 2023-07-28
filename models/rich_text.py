"""
Rich text objects

https://developers.notion.com/reference/rich-text
"""

from pydantic import HttpUrl
from .base_model import NotionObjectModel, NotionBaseModel
from .base_object import UrlObject, DateObject
from .user import User
from typing import Union, Literal
from enum import Enum

__all__ = (
    "TextColor",
    "Annotation",
    "EquationText",
    "MentionText",
    "Text", 
    "RichText",
)

class TextColor(Enum):
    blue = "blue"
    blue_background = "blue_background"
    brown = "brown"
    brown_background = "brown_background"
    default = "default"
    gray = "gray"
    gray_background = "gray_background"
    green = "green"
    green_background = "green_background"
    orange = "orange"
    orange_background = "orange_background"
    pink = "pink"
    pink_background = "pink_background"
    purple = "purple"
    purple_background = "purple_background"
    red = "red"
    red_background = "red_background"
    yellow = "yellow"
    yellow_background = "yellow_background"

class Annotation(NotionBaseModel):
    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    underline: bool = False
    code: bool = False
    color: TextColor = TextColor.default

class BaseRichText(NotionBaseModel):
    annotations: Annotation
    plain_text: str
    href: None | HttpUrl


""" Equation text """

class EquationContent(NotionBaseModel):
    expression: str

class EquationText(BaseRichText):
    type: Literal["equation"]
    equation: EquationContent


""" Mention text """

class DatabaseMention(NotionBaseModel):
    type: Literal["database"]
    database: NotionObjectModel

class DateMention(NotionBaseModel):
    type: Literal["date"]
    date: DateObject

class LinkPreviewMention(NotionBaseModel):
    type: Literal["link_preview"]
    link_preview: UrlObject

class PageMention(NotionBaseModel):
    type: Literal["page"]
    page: NotionObjectModel

class TemplateMentionDateType(Enum):
    today = "today"
    now = "now"

class TemplateMentionDate(NotionBaseModel):
    type: Literal["template_mention_date"]
    template_mention_date: TemplateMentionDateType

class TemplateMentionUserType(Enum):
    me = "me"

class TemplateMentionUser(NotionBaseModel):
    type: Literal["template_mention_user"]
    template_mention_user: TemplateMentionUserType

TemplateMentionDetail = Union[
    TemplateMentionDate,
    TemplateMentionUser
]

class TemplateMention(NotionBaseModel):
    type: Literal["template_mention"]
    template_mention: TemplateMentionDetail

class UserMention(NotionBaseModel):
    type: Literal["user"]
    user: User

MentionType = Union[
    DatabaseMention,
    DateMention,
    LinkPreviewMention,
    PageMention,
    TemplateMention,
    UserMention
]

class MentionText(BaseRichText):
    type: Literal["mention"]
    mention: MentionType


""" Normal text """

class TextContent(NotionBaseModel):
    content: str
    link: None | UrlObject

class Text(BaseRichText):
    type: Literal["text"]
    text: TextContent



RichText = Union[
    Text,
    MentionText,
    EquationText,
]

def _rich_text_finder(obj):
    class RichTextFinder(NotionBaseModel):
        detected: RichText
    return RichTextFinder(**obj).detected

    