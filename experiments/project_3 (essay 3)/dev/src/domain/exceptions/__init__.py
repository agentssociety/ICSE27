from __future__ import annotations

"""
Public exception API for shared.exceptions.

Import from this module for convenience:
    from src.domain.exceptions.exceptions import SomeException

Or import directly from the domain-specific module:
    from src.domain.exceptions.exceptions.city_exceptions import CityNotFoundException
"""

from .flight_exceptions import AmbiguousFlightClassificationException
from .shared_exceptions import ApiUnavailableException, AuthenticationException, AuthenticationFailedException, AuthenticationRequiredException, AuthorizationException, DatabaseException, DoubleBookingException, InsufficientPermissionException, InvalidStateTransitionException, ResourceNotAccessibleException, UnauthorizedException, UnauthorizedOperationException
from .slot_exceptions import NoScheduledSlotsException, SlotOverlapException, SlotUnavailableException

__all__ = [
    "AmbiguousFlightClassificationException",
    "ApiUnavailableException",
    "AuthenticationException",
    "AuthenticationFailedException",
    "AuthenticationRequiredException",
    "AuthorizationException",
    "DatabaseException",
    "DoubleBookingException",
    "InsufficientPermissionException",
    "InvalidStateTransitionException",
    "NoScheduledSlotsException",
    "ResourceNotAccessibleException",
    "SlotOverlapException",
    "SlotUnavailableException",
    "UnauthorizedException",
    "UnauthorizedOperationException",
]