from .base_builder import *
from .helper import nothing
from ..models.user import *

class UserBuilder(BaseBuilder):
    """
    Usage example:
    ```py
    class MyUserBuilder(UserBuilder):
        id = "87a790a9-aa6b-4fa4-b615-71d0a5390aa8"

    database.edit(builder=MyDatabaseBuilder())
    ```

    You can also instantiate Builder class as following.
    ```
    builder = DatabaseBuilder.set_from(
        title = "database title",
        description = "here is description",
        icon = "📛",
    )

    database.edit(builder=builder)
    ```
    """
    
    fields_setting = {
        "id": {
            str: nothing,
            People: lambda x: str(x.id),
            Bot: lambda x: str(x.id),
            BaseUser: lambda x: str(x.id),
        },
    }
    
    def build(self):
        return {
            "object": "user",
            "id": self.fields_value["id"]
        }
