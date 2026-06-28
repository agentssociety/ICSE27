from __future__ import annotations

from typing import Any

"""
Exceptions for the slot domain

Package: shared.exceptions
Layer: domain
Related tasks: None
"""

class NoAvailableSlotException(Exception):
    def __init__(self, message: str | None = None) -> None:
        self.message = message
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"NoAvailableSlotException(message={self.message!r})"

class NoSlotAvailableException(Exception):
    def __init__(self, message: str | None = None) -> None:
        self.message = message
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"NoSlotAvailableException(message={self.message!r})"

class SlotAllocationException(Exception):
    def __init__(self, reason: str | None = None) -> None:
        self.reason = reason
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"SlotAllocationException(reason={self.reason!r})"