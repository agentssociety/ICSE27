from __future__ import annotations

from typing import Any, Optional, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.user import Bool, IfaceKind

"""
Repository layer for the Pin domain class

Package: repository.pin
Layer: repository
Related tasks: #88
Requirement coverage:
- Card and PIN Authentication Requirement
"""

from src.dto.pin.pin_dto import PinCreateRequest, PinUpdateRequest, PinResponse


class Interface(Protocol):
    def get_by_id(self, item_id: str) -> Optional[PinResponse]: ...
    def get_all(self, skip: int = 0, limit: int = 100) -> list[PinResponse]: ...
    def create(self, data: PinCreateRequest) -> PinResponse: ...
    def update(self, item_id: str, data: PinUpdateRequest) -> Optional[PinResponse]: ...
    def delete(self, item_id: str) -> bool: ...


class CardReader(Protocol):
    def readCard(self, cardData: Any) -> None:
        ...


class PINVerificationService(Protocol):
    def verify_pin(self, user_id: str, pin: str) -> bool:
        ...
