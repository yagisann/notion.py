from .base_builder import BaseBuilder, _FieldUndefined
from .database_property import DatabasePropertyBuilder
from .helper import icon_parser, text_parser, file_parser, nothing



class DatabaseBuilder(BaseBuilder):
    __doc__ = """
Usage example:
```py
import notion
from notion.builder import DatabaseBuilder

client = notion.Client(token="your token here")
database = await client.fetch_database("42740044-ebe2-432a-8206-d806bfd41689")

class MyDatabaseBuilder(DatabaseBuilder):
    title = "database title"
    description = "here is description"
    icon = "📛"

database.edit(builder=MyDatabaseBuilder())
```

You can instantiate Builder class alternatively as following.
```py
builder = DatabaseBuilder.set_from(
    title = "database title",
    description = "here is description",
    icon = "📛",
)

await database.edit(builder=builder)
```
    """

    fields_setting = {
        "title": text_parser,
        "description": text_parser,
        "icon": icon_parser,
        "cover": file_parser,
        "is_inline": {bool: nothing},
    }

    def build(self):
        return {i: j for i,j in self.fields_value.items() if not isinstance(j, _FieldUndefined)}