"""
User objects

https://developers.notion.com/reference/user
"""

from .base_model import NotionObjectModel, NotionBaseModel
from .general_object import EmailObject, EmptyObject
from typing import Literal, Any, Union

__all__ = (
    "People",
    "Bot",
    "BaseUser",
    "User",
)

class BaseUser(NotionObjectModel):
    object: Literal["user"]

    @classmethod
    def new(cls, uid: str):
        return cls(id=uid, object="user")

class People(BaseUser):
    type: Literal["person"]
    name: str
    avatar_url: str | None
    person: EmailObject | EmptyObject

class BotWorkspaceOwner(NotionBaseModel):
    type: Literal["workspace"]
    workspace: bool

class BotUserOwner(NotionBaseModel):
    """
    this model should be update in future. I have not see 'user' type owner.
    """
    type: Literal["user"]
    user: Any

class BotProperty(NotionBaseModel):
    """
    owner should be an enum of 'workspace' or 'user', but I have not see 'user' type owner.
    """
    owner: BotWorkspaceOwner | BotUserOwner
    workspace_name: str | None

class Bot(BaseUser):
    type: Literal["bot"]
    name: str
    avatar_url: str | None
    bot: BotProperty

User = Union[
    People,
    Bot,
    BaseUser,
]
