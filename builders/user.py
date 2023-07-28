from .base_builder import *
from ..models.user import *

class UserBulider(BaseBuilder):
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
            str: lambda x: x,
            People: lambda x: str(x.id),
            Bot: lambda x: str(x.id),
            BaseUser: lambda x: str(x.id),
        },
    }
    
    def build(self):
        self.check_fields_exist()
        return {
            "object": "user",
            "id": fields_value["id"]
        }
