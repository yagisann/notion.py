class NotionBaseException(Exception):
    pass

class UnUpdatableError(NotionBaseException):
    pass

class ClientMissingError(NotionBaseException):
    pass