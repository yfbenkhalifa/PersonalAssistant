from overrides import overrides


class ServerException(Exception):
    """Base class for server-related exceptions."""
    @overrides
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message