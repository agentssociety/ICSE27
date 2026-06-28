from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.slot import Slot

"""
Exceptions for the slot domain

Package: shared.exceptions
Layer: domain
Related tasks: None
"""

class NoScheduledSlotsException(Exception):
    def __init__(self) -> None:
        super().__init__("NoScheduledSlotsException")

    def __str__(self) -> str:
        return "NoScheduledSlotsException"

class SlotOverlapException(Exception):
    def __init__(self) -> None:
        super().__init__("SlotOverlapException")

    def __str__(self) -> str:
        return "SlotOverlapException"

class SlotUnavailableException(Exception):
    def __init__(self, message: str | None = None, slot: Slot | None = None) -> None:
        self.message = message
        self.slot = slot
        super().__init__(self.__str__())

    def __str__(self) -> str:
        return f"SlotUnavailableException(message={self.message!r}, slot={self.slot!r})"