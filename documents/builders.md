# Notion.py Model Builder

## What is Builder?
---
Notion.py has couple of main feature models, 'Model' and 'Builder'. 'Model' (notion.models) is used to perse and validate Notion API payloads. On the other hand, 'Builder' (notion.builders) is used to building request payloads for Notion API.

## How to build Builders

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

- ### Create database
    ```py
    import notion
    from notion.builders import *

    project_options = SelectOptionsBuilder([
        "Proj-x", # color will be set automatically.
        OptionBuilder(name="Proj-Lemon", color="yellow"),
        OptionBuilder(name="Proj-Apple", color="red"),
        OptionBuilder(name="Proj-Melon", color="green"),
    ])

    property_builder = DatabasePropertyBuilder(
        columns={
            "task name": TitleColumn(),
            "project": MultiSelectColumn(multi_select=project_options)
            "assigned": PeopleColumn(),
            "until": DateColumn(),
        }
    )


    client = notion.Client(token="your token here")
    new_ database = await client.create_database(
        builder=DatabaseBuilder(title="Projects Overview", description="summation of tasks."),
        properties=property_builder,
        parent=PageParentBuilder(page_id="e256186b-f566-4e3c-9bb7-bf7f0d4ac20a")
    )
    ```
    ---
- ### Update database
    ```py
    import notion
    from notion.builders import DatabaseBuilder, DatabasePropertyBuilder

    client = notion.Client(token="your token here")
    database = await client.fetch_database("42740044-ebe2-432a-8206-d806bfd41689")

    property_builder = DatabasePropertyBuilder(model_db=database.properties)
    property_builder.add_columns({
        "last edit": LastEditedBy()
    })
    property_builder["assingned"].remove = True
    property_builder["project"].rename = "parent"

    await database.edit(properties=property_builder)
    ```
    ---
- ### Create page under page
    ```py
    import notion
    from notion.builders import PageBuilder, PagePropertyBuilder, PageParentBuilder, Title

    properties = PagePropertyBuilder(
        title="Page title"
    )

    client = notion.Client(token="your token here")
    new_page = await client.create_page(
        builder=PageBuilder(),
        properties=properties,
        parent = PageParentBuilder(page_id="e256186b-f566-4e3c-9bb7-bf7f0d4ac20a")
    )
    ```
    ---
- ### Create page under database
    ```py
    import notion
    from notion.builders import *

    client = notion.Client(token="your token here")
    database = await client.fetch_database("42740044-ebe2-432a-8206-d806bfd41689")

    properties = PagePropertyBuilder(
        title="New Page",
        values = {
            "project": MuitiSelect(["Proj-Lemon", "Proj-Melon"]),
            "assigned": People("54679f9f-1c66-40c5-956f-046691769ee1"), # user UUID
        }
    )

    new_page = await database.create_page(
        builder=PageBuilder(),
        properties=properties
    )
    ```
    ---
- ### Update page
    ```py
    import notion
    from notion.builders import PageBuilder, PagePropertyBuilder

    client = notion.Client(token="your token here")
    page = await client.fetch_page("e256186b-f566-4e3c-9bb7-bf7f0d4ac20a")

    property_builder = PagePropertyBuilder(model_page=page.properties)
    property_builder.edit(
        title="New title",
        values = {
            "project": MultiSelect(["Proj-x"]),
            "is_checked": CheckBox(False)
        }
    )

    await page.edit(properties=property_builder)
    ```
