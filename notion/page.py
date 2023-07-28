from .models import Page as PageModel
from .builders import PageBuilder, PagePropertyBuilder


class Page:

    def __init__(self, *, client, data):
        self.client = client
        self.model = PageModel(**data)