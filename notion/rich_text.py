"""
Rich text objects

https://developers.notion.com/reference/rich-text
"""

from pydantic import HttpUrl
from .base_model import NotionObjectModel, NotionBaseModel
from .general_object import UrlObject, DateObject
from .user import User, BaseUser
from typing import Union, Literal
from enum import Enum
from datetime import datetime as dt

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

    @classmethod
    def new(cls, expression: str = ""):
        return cls(
            annotations=Annotation(),
            plain_text="",
            href=None,
            type="equation",
            equation=EquationContent(expression=expression)
        )


""" Mention text """


class DatabaseMention(NotionBaseModel):
    type: Literal["database"]
    database: NotionObjectModel

    @classmethod
    def new(cls, database_id: str):
        return cls(type="database", database=NotionObjectModel(id=database_id))


class DateMention(NotionBaseModel):
    type: Literal["date"]
    date: DateObject

    @classmethod
    def new(
        cls,
        start: None | dt,
        end: None | dt = None,
        time_zone: None | str = None,
    ):
        return cls(type="date", date=DateObject(start=start, end=end, time_zone=time_zone))


class LinkPreviewMention(NotionBaseModel):
    type: Literal["link_preview"]
    link_preview: UrlObject

    @classmethod
    def new(cls, url: str):
        return cls(type="link_preview", link_preview=UrlObject(url=url))


class PageMention(NotionBaseModel):
    type: Literal["page"]
    page: NotionObjectModel

    @classmethod
    def new(cls, page_id: str):
        return cls(type="page", page=NotionObjectModel(id=page_id))


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

    @classmethod
    def new(cls, mention_target: str):
        if mention_target in TemplateMentionDateType.__menbers__:
            return cls(type="template_mention", template_mention=TemplateMentionDate(type="template_mention_date", template_mention_date=mention_target))
        if mention_target in TemplateMentionUserType.__members__:
            return cls(type="template_mention", template_mention=TemplateMentionUser(type="template_mention_user", template_mention_user=mention_target))
        raise ValueError("mention_target should be one of "+str(
            [*TemplateMentionDateType.__menbers__, *TemplateMentionUserType.__members__]))


class UserMention(NotionBaseModel):
    type: Literal["user"]
    user: User

    @classmethod
    def new(cls, uid: str):
        return cls(type="user", user=BaseUser.new(uid=uid))


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

    @classmethod
    def new(cls, montion_model: MentionType):
        return cls(
            annotations=Annotation(),
            plain_text="",
            href=None,
            type="mention",
            mention=montion_model,
        )


""" Normal text """


class TextContent(NotionBaseModel):
    content: str
    link: None | UrlObject

    @classmethod
    def new(cls, text: str = "", url: None | str = None):
        return cls(content=text, link=url)


class Text(BaseRichText):
    type: Literal["text"]
    text: TextContent

    @classmethod
    def new(cls, text: str = "", url=None):
        return cls(
            annotations=Annotation(),
            plain_text=text,
            href=None,
            type="text",
            text=TextContent.new(text, url),
        )


RichText = Union[
    Text,
    MentionText,
    EquationText,
]


def _rich_text_finder(obj):
    class RichTextFinder(NotionBaseModel):
        detected: RichText
    return RichTextFinder(**obj).detected
