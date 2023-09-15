from .models import Page as PageModel

__all__ = (
    "get_page_title",
)

def get_page_title(page: PageModel):
    titletext_array = [i.title for i in page.properties.values() if i.id == "title"][0]
    return "".join([i.plain_text for i in titletext_array])
