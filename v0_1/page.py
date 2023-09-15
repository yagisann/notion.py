from .models import Page as PageModel
from .builders import PageBuilder, PagePropertyBuilder
from.utils import NotionObject


class Page(NotionObject):

    def __init__(self, *, client, data):
        super().__init__()
        super().__setattr__("initialized", False)
        self.client = client
        self.model_dict = data
        self.model = PageModel(**data)
        self.client.cache.pages.add(self)
        self.properties = self.model.properties
        self.initialized=True

    def __getattr__(self, key):
        try:
            return super().__getattribute__(key)
        except AttributeError:
            if key in self.model_dict:
                return self.model_dict[key]
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")
    
    def __getitem__(self, key):
        if key in self.model_dict["properties"]:
            return self.model_dict["properties"][key]
        raise KeyError(f"'{self.__class__.__name__}' instance has no property named '{key}'")
    
    def __setattr__(self, key, val):
        if not self.initialized:
            super().__setattr__(key, val)
            return
        if key in self.model_dict:
            return NotImplementedError()
        super().__setattr__(key, val)
        
    def __setitem__(self, key, val):
        raise NotImplementedError()


    async def update(self):
        self.model_dict = await self.client.pages.retrieve(page_id=self.id)
        self.model = PageModel(**self.model_dict)
        return self
    
    async def edit(self, builder=None, properties=None):
        if not isinstance(builder, (PageBuilder, type(None))):
            raise TypeError("builder argument must be object of PageBuilder")
        if not isinstance(properties, (PagePropertyBuilder, type(None))):
            raise TypeError("properties argument must be object of PagePropertyBuilder")
        if not (builder or properties):
            return
        payload = {"page_id": str(self.model.id)}
        if builder:
            payload.update(builder.build())
        if properties:
            payload["properties"] = properties.build()
        self.model_dict = await self.client.pages.update(**payload)
        self.model = PageModel(**self.model_dict)
        return self
    
    async def archive(self):
        payload = {"page_id": str(self.model.id)}
        payload["archived"] = True
        self.model_dict = await self.client.pages.update(**payload)
        self.model = PageModel(**self.model_dict)
    
    async def restore(self):
        payload = {"page_id": str(self.model.id)}
        payload["archived"] = False
        self.model_dict = await self.client.pages.update(**payload)
        self.model = PageModel(**self.model_dict)