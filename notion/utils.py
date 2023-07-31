from typing import Any, Dict
from .notion_client.errors import HTTPResponseError, RequestTimeoutError, APIErrorCode, APIResponseError
import random, asyncio


class NotionObject():
    def __init__(self):
        super().__setattr__("initialized", False)
        self.model_dict = None
        self.model = None
        self.client = None
    

def pick(base: Dict[Any, Any], *keys: str) -> Dict[Any, Any]:
    """Return a dict composed of key value pairs for keys passed as args."""
    return {key: base[key] for key in keys if key in base}

def exponential_backoff(base_sec=1, max_backoff=600):
    """Exponential backoff and jitter"""
    attempt = 0
    while 1:
        c = base_sec*2**attempt
        backoff = c if c < max_backoff else max_backoff
        sleep = backoff + random.uniform(-backoff/10, backoff/10)
        yield sleep
        attempt += 1
"""
class RetryHandler:

    def __init__(self, coro, args):
        self.backoff = exponential_backoff()
        self.coro = coro
        self.args = args
    
    async def run(self):
        while 1:
            try:
                return await self.coro(**self.args)
            except APIResponseError as e:
                b = self.backoff.__next__()
                print(f"[An error occurred while requesting database. Error code: {e.code}. retry in {b} seconds.")
                await asyncio.sleep(b)

            except RequestTimeoutError as e:
                b = self.backoff.__next__()
                print(f"[An error occurred while requesting database. Error: request timeout. retry in {b} seconds.")
                await asyncio.sleep(b)
            except HTTPResponseError as e:
                b = self.backoff.__next__()
                print(f"[An error occurred while requesting database. Error code: {e.status} retry in {b} seconds.")
                await asyncio.sleep(b)
"""

class DictDotNotation:
    def __init__(self, *args, **kwargs):
        for i in args:
            if not isinstance(i, dict):
                raise ValueError(f"To instantiate 'DictDotNotation' object, argument must be 'dict' object")
            for key, val in i.items():
                if isinstance(val, dict):
                    val = DictDotNotation(val)
                setattr(self, key, val)
        for key, val in kwargs.items():
            if isinstance(val, dict):
                val = DictDotNotation(val)
            setattr(self, key, val)
    
    def __getitem__(self, val):
        return getattr(self, val)
    
    def __setitem__(self, key, val):
        setattr(self, key, val)
    
    def __getattr__(self, key):
        return None
    
    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self, *args, **kwargs):
        return self.__dict__.items(*args, **kwargs)

    def __len__(self):
        return self.__dict__.__len__()
    
    def __repr__(self):
        return f"DictDotNotation({self.__dict__})"
    
    def __str__(self):
        return str(self.to_flatdict())
    
    def to_flatdict(self):
        return_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, DictDotNotation):
                value = value.to_flatdict()
            return_dict[key] = value
        return return_dict
    
    def copy(self):
        return DictDotNotation(self.to_flatdict())