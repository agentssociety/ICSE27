from __future__ import annotations

from typing import Any

"""
Exceptions for the flight domain

Package: shared.exceptions
Layer: domain
Related tasks: None
"""

class AmbiguousFlightClassificationException(Exception):
    def __init__(self, flightId: str | None = None) -> None:
        self.flightId = flightId
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"AmbiguousFlightClassificationException(flightId={self.flightId!r})"