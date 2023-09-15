from .models import (
    People as PeoplePayload,
    Bot as BotPayload,
    BaseUser as BaseUserPayload,
)

class BaseUser:

    def __init__(self, data, client):
        self.client = client
        self.payload_type = BaseUserPayload
        self._form_data(BaseUserPayload(**data))
    
    def _form_data(self, data: BaseUserPayload):
        self.id = data.id
        self.object = data.object
    
    def __eq__(self, other):
        if isinstance(other, self.payload_type):
            return self.id == other.id
        return NotImplemented
    
    def __repr__(self):
        attrs = [
            ('object', self.object),
            ('id', self.id),
        ]
        joined = ' '.join('%s=%r' % t for t in attrs)
        return f'<{self.__class__.__name__} {joined}>'
    