from __future__ import annotations

from typing import Any, Optional, Protocol

from src.dto.card.card_dto import CardCreateRequest, CardUpdateRequest, CardResponse

"""
Service layer for the Card domain class

Package: service.card
Layer: service
Related tasks: #88
Requirement coverage:
- Card and PIN Authentication Requirement
"""


class CardService(Protocol):
    def create_card(self, data: CardCreateRequest) -> CardResponse: ...
    def get_card(self, card_id: str) -> Optional[CardResponse]: ...
    def get_all_cards(self, skip: int = 0, limit: int = 100) -> list[CardResponse]: ...
    def update_card(self, card_id: str, data: CardUpdateRequest) -> Optional[CardResponse]: ...
    def delete_card(self, card_id: str) -> bool: ...


class CardServiceImpl:
    def __init__(self, repository: Any) -> None:
        self._repository = repository

    def create_card(self, data: CardCreateRequest) -> CardResponse:
        return self._repository.create(data)

    def get_card(self, card_id: str) -> Optional[CardResponse]:
        return self._repository.get_by_id(card_id)

    def get_all_cards(self, skip: int = 0, limit: int = 100) -> list[CardResponse]:
        return self._repository.get_all(skip=skip, limit=limit)

    def update_card(self, card_id: str, data: CardUpdateRequest) -> Optional[CardResponse]:
        return self._repository.update(card_id, data)

    def delete_card(self, card_id: str) -> bool:
        return self._repository.delete(card_id)
