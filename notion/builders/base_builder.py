from typing import Callable

class _FieldUndefined:
    def __bool__(self):
        return 0

FieldUndefined = _FieldUndefined()

class BaseBuilder:
    fields_setting: dict[str, dict[type, Callable]] = dict()

    def __init__(self, **kw):
        self.fields_value = dict()
        try:
            self.default_value
        except AttributeError:
            self.default_value = dict()
        kwargs = dict()
        for key in self.fields_setting.keys():
            try:
                kwargs[key] = self.__getattribute__(key)
            except AttributeError:
                pass
            try:
                kwargs[key] = kw[key]
            except KeyError:
                pass
            try:
                self.default_value[key]
            except KeyError:
                self.default_value[key] = FieldUndefined
        self._form_data(kwargs)
    
    def __getitem__(self, key):
        return self.fields_value[key]
    
    def set_fields(self, **kwargs):
        self._form_data(kwargs, initialize=False)

    def initialize_fields(self, fields_list: list[str]):
        for key in fields_list:
            self.fields_value[key] = self.default_value[key]
    
    @classmethod
    def set_from(cls, ignore_extra=False, **kwargs):
        return cls()._form_data(kwargs, ignore_extra=ignore_extra)
    
    def _form_data(self, kwargs: dict, initialize: bool=True, ignore_extra=False):
        if initialize:
            for key in self.fields_setting.keys():
                self.fields_value[key] = self.default_value[key]
        for key, val in kwargs.items():
            if (key in self.fields_setting):
                if isinstance(val, tuple(self.fields_setting[key].keys())):
                    self.fields_value[key] = self.fields_setting[key][type(val)](val)
                else:
                    raise TypeError(f"Type of '{key}' must be one of {tuple(self.fields_setting[key].keys())}")
            else:
                if not ignore_extra:
                    raise KeyError(f"'{key}' is not valid key for {self.__class__.__name__}")
        return self
    
    def check_fields_exist(self, include: list=[], exclude: list=[]):
        if not include and not exclude:
            fields = list(self.fields_setting.keys())
        elif include and not exclude:
            fields = include
        elif include and exclude:
            include = include if include else self.fields_setting.keys()
            fields = [i for i in include if i not in exclude]
        undefined_fields = []
        for key in fields:
            if isinstance(self.fields_value[key], _FieldUndefined):
                undefined_fields.append(key)
        if undefined_fields:
            raise ValueError(f"The following field(s) must be specified: {', '.join(undefined_fields)}")