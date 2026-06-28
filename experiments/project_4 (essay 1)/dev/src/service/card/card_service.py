from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.infra.card.card_repo_impl import SQLAlchemyCardRepository


class AuthenticationFlow:
    def __init__(self, repo: SQLAlchemyCardRepository) -> None:
        self._repo = repo

    def authenticate(self, cardData: str, pinData: str) -> bool:
        return bool(cardData)

    def false(self, expired: Any) -> None:
        pass