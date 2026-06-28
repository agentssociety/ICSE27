from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.runway import Permission, State

"""
Exceptions for the shared domain

Package: shared.exceptions
Layer: domain
Related tasks: None
"""

class ApiUnavailableException(Exception):
    def __init__(self) -> None:
        super().__init__("ApiUnavailableException")

    def __str__(self) -> str:
        return "ApiUnavailableException"

class AuthenticationException(Exception):
    def __init__(self, message: str | None = None, timestamp: DateTime | None = None) -> None:
        self.message = message
        self.timestamp = timestamp
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"AuthenticationException(message={self.message!r}, timestamp={self.timestamp!r})"

class AuthenticationFailedException(Exception):
    def __init__(self) -> None:
        super().__init__("AuthenticationFailedException")

    def __str__(self) -> str:
        return "AuthenticationFailedException"

class AuthenticationRequiredException(Exception):
    def __init__(self, channelId: str | None = None) -> None:
        self.channelId = channelId
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"AuthenticationRequiredException(channelId={self.channelId!r})"

class AuthorizationException(Exception):
    def __init__(self, message: str | None = None, permissionRequired: Permission | None = None) -> None:
        self.message = message
        self.permissionRequired = permissionRequired
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"AuthorizationException(message={self.message!r}, permissionRequired={self.permissionRequired!r})"

class DatabaseException(Exception):
    def __init__(self) -> None:
        super().__init__("DatabaseException")

    def __str__(self) -> str:
        return "DatabaseException"

class DoubleBookingException(Exception):
    def __init__(self, message: str | None = None, conflictingRequests: FlightRequest | None = None) -> None:
        self.message = message
        self.conflictingRequests = conflictingRequests
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"DoubleBookingException(message={self.message!r}, conflictingRequests={self.conflictingRequests!r})"

class InsufficientPermissionException(Exception):
    def __init__(self, actorId: str | None = None, requiredPermission: Permission | None = None) -> None:
        self.actorId = actorId
        self.requiredPermission = requiredPermission
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"InsufficientPermissionException(actorId={self.actorId!r}, requiredPermission={self.requiredPermission!r})"

class InvalidStateTransitionException(Exception):
    def __init__(self, message: str | None = None, fromState: State | None = None, toState: State | None = None) -> None:
        self.message = message
        self.fromState = fromState
        self.toState = toState
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"InvalidStateTransitionException(message={self.message!r}, fromState={self.fromState!r}, toState={self.toState!r})"

class ResourceNotAccessibleException(Exception):
    def __init__(self, actorId: str | None = None, resourceId: str | None = None) -> None:
        self.actorId = actorId
        self.resourceId = resourceId
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"ResourceNotAccessibleException(actorId={self.actorId!r}, resourceId={self.resourceId!r})"

class UnauthorizedException(Exception):
    def __init__(self) -> None:
        super().__init__("UnauthorizedException")

    def __str__(self) -> str:
        return "UnauthorizedException"

class UnauthorizedOperationException(Exception):
    def __init__(self) -> None:
        super().__init__("UnauthorizedOperationException")

    def __str__(self) -> str:
        return "UnauthorizedOperationException"