from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.api.runway import Actor
    from src.domain.runway import Permission

"""
Exceptions for the shared domain

Package: shared.exceptions
Layer: domain
Related tasks: None
"""

class AuthenticationException(Exception):
    def __init__(self, message: str | None = None) -> None:
        self.message = message
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"AuthenticationException(message={self.message!r})"

class AuthenticationFailedException(Exception):
    def __init__(self, message: str | None = None) -> None:
        self.message = message
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"AuthenticationFailedException(message={self.message!r})"

class AuthorizationException(Exception):
    def __init__(self, actor: Actor | None = None, requiredPermission: Permission | None = None, message: str | None = None) -> None:
        self.actor = actor
        self.requiredPermission = requiredPermission
        self.message = message
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"AuthorizationException(actor={self.actor!r}, requiredPermission={self.requiredPermission!r}, message={self.message!r})"

class ConcurrentModificationException(Exception):
    def __init__(self, message: str | None = None) -> None:
        self.message = message
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"ConcurrentModificationException(message={self.message!r})"

class ResourceNotFoundException(Exception):
    def __init__(self, message: str | None = None) -> None:
        self.message = message
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"ResourceNotFoundException(message={self.message!r})"

class UnauthorizedAccessException(Exception):
    def __init__(self, message: str | None = None) -> None:
        self.message = message
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"UnauthorizedAccessException(message={self.message!r})"