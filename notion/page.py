from .models import Page as PageModel
from .builders import PageBuilder, PagePropertyBuilder


class Page:

    def __init__(self, *, client, data):
        self.client = client
        self.model = PageModel(**data)
        self.client.cache.pages.add(self)
        
    
    async def edit(self, builder=None, properties=None):
        if not isinstance(builder, (PageBuilder, type(None))):
            raise TypeError("builder argument must be object of PageBuilder")
        if not isinstance(properties, (PagePropertyBuilder, type(None))):
            raise TypeError("properties argument must be object of PagePropertyBuilder")
        if not (builder or properties):
            return
        payload = {"page_id": self.model.id}
        if builder:
            payload.update(builder.build())
        if properties:
            payload["properties"] = properties.build()
        new_model_data = await self.client.pages.update(**payload)
        self.model = PageModel(**new_model_data)
    
    async def archive(self):
        payload = {"page_id": self.model_id}
        payload["archived"] = True
        new_model_data = await self.client.pages.update(**payload)
        self.model = PageModel(**new_model_data)
    
    async def restore(self):
        payload = {"page_id": self.model_id}
        payload["archived"] = False
        new_model_data = await self.client.pages.update(**payload)
        self.model = PageModel(**new_model_data)