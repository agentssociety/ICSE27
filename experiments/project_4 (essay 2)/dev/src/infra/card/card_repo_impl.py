from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.card.card_dto import CardCreateRequest, CardUpdateRequest, CardResponse
from src.orm.card.card_orm import CardORM

"""
Infra layer for the Card domain class

Package: infra.card
Layer: infra
Related tasks: #88
Requirement coverage:
- Card and PIN Authentication Requirement
"""


class SQLAlchemyCardRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: str) -> Optional[CardResponse]:
        row = self._session.get(CardORM, item_id)
        return CardResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[CardResponse]:
        rows = self._session.query(CardORM).offset(skip).limit(limit).all()
        return [CardResponse.model_validate(r) for r in rows]

    def create(self, data: CardCreateRequest) -> CardResponse:
        row = CardORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return CardResponse.model_validate(row)

    def update(self, item_id: str, data: CardUpdateRequest) -> Optional[CardResponse]:
        row = self._session.get(CardORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return CardResponse.model_validate(row)

    def delete(self, item_id: str) -> bool:
        row = self._session.get(CardORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
