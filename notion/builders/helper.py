from ..models.rich_text import *
from ..models.emoji import Emoji
from ..models.database import Database
from ..models.database_property import RollupFunctionType
from ..models.base_object import SelectOption
from ..models.user import BaseUser
from ..models.enums import Color
from ..models.file import NotionHostedFile, ExternalFile, File

import emoji
from urllib.parse import urlparse

nothing = lambda x: x

def url_detector(i: str):
    if len(urlparse(i).scheme):
        return i
    else:
        raise ValueError("Provided string is not valid url")

def icon_detector(i: str):
    if emoji.is_emoji(i):
        return {"emoji": i}
    elif len(urlparse(i).scheme):
        return {"external": {"url": i}}
    else:
        raise ValueError("Provided string is not valid url or emoji")

def text_list_detector(i: list[Text]):
    if all([isinstance(j, (Text)) for j in i]):
        return [j.model_dump(include=("text")) for j in i]
    else:
        raise ValueError("Provided list should be list of Text object")


def new_text(content):
    return Text(
        type="text",
        annotations=Annotation(),
        plain_text=content,
        href=None,
        text={
            "content": content,
            "link": None
        }
    )

def new_file(url):
    return ExternalFile(
        type="external",
        external={"url": url}
    )


text_parser = {
    str: lambda x: [new_text(x).model_dump(include=("text"))],
    Text: lambda x: [x.model_dump(include=("text"))],
    list: text_list_detector,
}

icon_parser = {
    type(None): nothing,
    str: icon_detector,
    Emoji: lambda x: x.model_dump(include=("emoji")),
    ExternalFile: lambda x: x.model_dump(include=("external")),
    NotionHostedFile: lambda x: {"external": {"url": x.file.url}},
}

file_parser = {
    type(None): nothing,
    str: lambda x: {"external": {"url": url_detector(x)}},
    ExternalFile: lambda x: x.model_dump(include=("external")),
    NotionHostedFile: lambda x: {"external": {"url": x.file.url}},
}

def files_list_parser(i: list):
    out = []
    for file in i:
        if isinstance(file, str):
            out.append(new_file(url_detector(file)))
        elif isinstance(file, (ExternalFile, NotionHostedFile,)):
            out,append(file)
        else:
            raise TypeError("file should be types of str, models.ExternalFile, models.NoionHostedFile")
    return out

files_parser = {
    str: lambda x: [new_file(url_detector(x))],
    list: lambda x: files_list_parser(x),
    NotionHostedFile: lambda x: [x],
    ExternalFile: lambda x: [x],
}


class OptionBuilder:

    def __init__(self, name, id=None, color=None):
        self.name = name
        self.id = id
        self._color = None
        self.color = color
    
    def __str__(self):
        return f"OptionBuilder(name={self.name}, id={self.id}, color={self._color})"
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, val):
        if val is None:
            self._color = None
        else:
            self._color = Color(val).value
    
    def build(self, include_color=True):
        payload = {"name": self.name}
        if self.color:
            payload["color"] = self.color
        return payload

class SelectOptionsBuilder:

    def __init__(self, options: list=[]):
        self.option_list = []
        for i in options:
            if isinstance(i, str):
                self.option_list.append(OptionBuilder(i))
            elif isinstance(i, OptionBuilder):
                self.option_list.append(i)
            elif isinstance(i, SelectOption):
                self.option_list.append(OptionBuilder(name=i.name, color=i.color.value))
            else:
                raise ValueError("SelectOptionsBuilder' argument, 'options' should be list of 'str', 'OptionBuilder', 'SelectOption'")
    
    def build(self, include_color=True):
        return [i.build(include_color) for i in self.option_list]

class RollupConfig:

    def __init__(self,
        function=None,
        relation_property_id=None,
        relation_property_name=None,
        rollup_property_id=None,
        rollup_property_name=None
    ):
        self._function = None
        self.function = function
        self.rel_id = relation_property_id
        self.rel_name = relation_property_name
        self.rol_id = rollup_property_id
        self.rol_name = rollup_property_name
        self.fields = ["function", "rollup_property_id", "rollup_property_name", "relation_property_id", "relatio_property_name"]
    
    @property
    def function(self):
        return self._function
    
    @function.setter
    def function (self, val):
        if (val is None):
            self._function = val
        else:
            self._function = RollupFunctionType(val).value
        
    def build(self):
        e = []
        if not (self.rel_id or self.rel_name):
            e.append("One of relation_property_name or relation_property_id must be provided.")
        if not (self.rol_id or self.rol_name):
            e.append("One of rollup_property_name or rollup_property_id must be provided.")
        if e:
            raise ValueError("\n".join(e))
        return {i: self.__getattribute__(i) for i in self.fields if self.__getattribute__(i) is not None}
        
