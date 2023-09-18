class NotionBaseException(Exception):
    pass

class UnUpdatableError(NotionBaseException):
    pass

class ClientMissingError(NotionBaseException):
    pass

class NotionValidationError(NotionBaseException):
    pass

class FieldMissingError(NotionBaseException):
    pass