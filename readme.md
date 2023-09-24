# Notion.py
An asynchronous api wrapper and data models for Notion API using pydantic.

## Notice 
<span style="color: red;">**This module is under development.**</span>
<br>currently, notion.py provides wrapper for notion database and page.

## Installation

**Python 3.11 or higher is required**

```sh
pip install git+https://github.com/yagisann/notion.py
```


## Quickstart
### Fetch page, create database under page
```py
import notion, asyncio
from notion.draft import DatabaseDraft, PageDraft

async def main():
    client = notion.Client(token="your_token")
    page = await client.fetch_page("your_page_id")

    # You can add database under page!
    draft = DatabaseDraft(
        title="this is example database", # required
        parent=page,                      # required
        description="added via api",
        icon="🤖",
        is_inline=True
    )
    db = await draft.create(client)

    # Also, you can add page under database!
    draft = PageDraft(
        title="this is example page",     # required
        parent=db,                        # required
    )

if __name__=="__main__":
    asyncio.run(main())
```
### Modifying database
```py
import notion, asyncio
from notion.database_property import LastEditedTime, Select, Date, Number

async def main():
    client = notion.Client(token="your_token")
    database = await client.fetch_database("your_database_id")

    # Modifying database meta data
    database.edit(
        title="modified title",
        description="modified description",
        icon="💫",
        cover="https://unsplash.com/photos/Yj-yqaGWKMg/download", # URL of image
        is_inline=False,
    )

    # Adding properties to the database
    database.add_property(name="Last edit", column=LastEditedTime.new())
    select = Select.new(
        options=["proj-alpha", "proj-beta", "proj-gamma"]
    )
    database.add_property(name="Project", column=select)
    database.add_property(name="Project start", column=Date.new())
    database.add_property(name="Budget", column=Number.new(format="dollar"))
    # Control of column ordering is currently not supported.

    # Pushing changes
    await database.update()

if __name__=="__main__":
    asyncio.run(main())
```

### Modifying page
```py
import asyncio, notion, datetime

async def test():
    client = notion.Client(token="your_token")
    page = await client.fetch_page("your_page_id")

    # Modifying page meta data
    page.edit(
        title="modified title",
        icon="💫",
        cover="https://unsplash.com/photos/qToVxSYXPYU/download", # URL of image
    )


    # Modifying page properties
    # You can use index notation to access properties.
    page["Project"].set_option(option="proj-beta")
    page["Project start"].start = datetime.datetime.now()
    page["Budget"].number = 5000

    # Pushing changes
    await page.update()

    # archive page
    await page.archive()


if __name__ == "__main__":
    asyncio.run(test())
```


## API Documents Link

- [Official Notion API documentations.](https://developers.notion.com/)
- [A summary of Official API docs](./documents/official_documents.md)


## TODO

- Search filter
    - querying to API
    - querying to cached object (like Database.pages.search())
- Block objects
- Comment objects
- logging
- API call optimization
    - add last_fetched attribute to objects
    - cache improvement (add gc)
- ...