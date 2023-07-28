from .models.rich_text

class BaseBuilder:
    finder: dict[str, type] = dict()
    
    def __init__(self, **kwargs):
        for key in self.finder.keys():
            self.__setattr__(key, ...)
        for key, value in kwargs.items():
            self.__setitem__(key, value)
        
    def __setitem__(self, key, value):
        if key in self.finder.keys():
            self._form_field(key, value)
        else:
            raise RuntimeError(f"'{key}' is uneditable property in {self.__class__.__name__}")
    
    @property
    def payload(self):
        p = dict()
        for key in self.finder.keys():
            if (v := self.__getattribute__(key)) is not ...:
                p[key] = v
        return p


class TextBulder:
