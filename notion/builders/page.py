from .base_builder import *
from .page_property import PagePropertyBuilder
from .helper import icon_parser, file_parser


class PageBuilder(BaseBuilder):
    fields_setting = {
        "archived": {bool: lambda x: x},
        "icon": icon_parser,
        "cover": file_parser,
    }

    def build(self):
        return {i: j for i,j in self.fields_value.items() if not isinstance(j, FieldUndefined)}
