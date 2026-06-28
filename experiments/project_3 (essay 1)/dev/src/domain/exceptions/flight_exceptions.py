from __future__ import annotations

from typing import Any

"""
Exceptions for the flight domain

Package: shared.exceptions
Layer: domain
Related tasks: None
"""

class DuplicateFlightNumberException(Exception):
    def __init__(self, flightNumber: str | None = None) -> None:
        self.flightNumber = flightNumber
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"DuplicateFlightNumberException(flightNumber={self.flightNumber!r})"

class InvalidFlightDataException(Exception):
    def __init__(self, field: str | None = None, message: str | None = None) -> None:
        self.field = field
        self.message = message
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"InvalidFlightDataException(field={self.field!r}, message={self.message!r})"

class InvalidFlightException(Exception):
    def __init__(self, details: str | None = None) -> None:
        self.details = details
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"InvalidFlightException(details={self.details!r})"
