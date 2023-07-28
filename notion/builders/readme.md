# Notion.py Model Builder

## What is Builder?
---
Notion.py has couple of main feature models, 'Model' and 'Builder'. 'Model' (notion.models) is used to perse and validate Notion API payloads. On the other hand, 'Builder' (notion.builders) is used to building request payloads for Notion API.

## How to build Builders
---
- ### basic instantiation method
    Builder has some fields and you can specify as a keyword arguments as following.
    ```py
    from notion.builders import DatabaseBuilder

    builder = DatabaseBuilder(
        title="database title",
        description="here is description",
        icon="㊨"
    )
    ```

## Usage example 
---
- ### Create database
    ```py
    import notion
    from notion.builder import *

    project_options = SelectOptionsBuilder([
        "Proj-x",
        OptionBuilder(name="Proj-Lemon", color="yellow"),
        OptionBuilder(name="Proj-Apple", color="red"),
        OptionBuilder(name="Proj-Melon", color="green"),
    ])

    columns = {
        "task name": TitleColumn(),
        "project": MultiSelectColumn(multi_select=project_options)
        "assigned": PeopleColumn(),
        "until": DateColumn(),
    }

    property_builder = DatabasePropertyBuilder(columns=columns)


    client = notion.Client(token="your token here")
    await client.create_database(
        builder=DatabaseBuilder(title="Projects Overview", description="summation of tasks."),
        properties=property_builder,
        parent=PageParentBuilder(page_id="e256186b-f566-4e3c-9bb7-bf7f0d4ac20a")
    )
    ```
    ---
- ### Update database
    ```py
    import notion
    from notion.builder import DatabaseBuilder, DatabasePropertyBuilder

    client = notion.Client(token="your token here")
    database = await client.fetch_database("42740044-ebe2-432a-8206-d806bfd41689")

    property_builder = DatabasePropertyBuilder(model_db=database.properties)
    property_builder.add_columns({
        "last edit": LastEditedBy
    })
    property_builder["assingned"].remove = True
    property_builder["project"].rename = "parent"

    await database.edit(properties=property_builder)
    ```
    ---
- ### Create page

- ### Update page

---
## Instantiate Builder
