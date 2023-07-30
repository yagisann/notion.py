from .base_builder import BaseBuilder, _FieldUndefined
from .page_property import PagePropertyBuilder
from .helper import icon_parser, file_parser, nothing


class PageBuilder(BaseBuilder):
    fields_setting = {
        "archived": {bool: nothing},
        "icon": icon_parser,
        "cover": file_parser,
    }

    def build(self):
        return {i: j for i,j in self.fields_value.items() if not isinstance(j, _FieldUndefined)}
