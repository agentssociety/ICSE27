from __future__ import annotations

from typing import Any, Optional, Protocol

from src.dto.pin.pin_dto import PinCreateRequest, PinUpdateRequest, PinResponse

"""
Service layer for the Pin domain class

Package: service.pin
Layer: service
Related tasks: #88
Requirement coverage:
- Card and PIN Authentication Requirement
"""


class PinService(Protocol):
    def create_pin(self, data: PinCreateRequest) -> PinResponse: ...
    def get_pin(self, pin_id: str) -> Optional[PinResponse]: ...
    def get_all_pins(self, skip: int = 0, limit: int = 100) -> list[PinResponse]: ...
    def update_pin(self, pin_id: str, data: PinUpdateRequest) -> Optional[PinResponse]: ...
    def delete_pin(self, pin_id: str) -> bool: ...


class PinServiceImpl:
    def __init__(self, repository: Any) -> None:
        self._repository = repository

    def create_pin(self, data: PinCreateRequest) -> PinResponse:
        return self._repository.create(data)

    def get_pin(self, pin_id: str) -> Optional[PinResponse]:
        return self._repository.get_by_id(pin_id)

    def get_all_pins(self, skip: int = 0, limit: int = 100) -> list[PinResponse]:
        return self._repository.get_all(skip=skip, limit=limit)

    def update_pin(self, pin_id: str, data: PinUpdateRequest) -> Optional[PinResponse]:
        return self._repository.update(pin_id, data)

    def delete_pin(self, pin_id: str) -> bool:
        return self._repository.delete(pin_id)
