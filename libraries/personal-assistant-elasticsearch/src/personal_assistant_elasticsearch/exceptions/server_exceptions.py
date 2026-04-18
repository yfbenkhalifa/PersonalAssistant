"""Shared server-side exceptions."""


class ServerException(Exception):
    """Base class for server-related exceptions."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

