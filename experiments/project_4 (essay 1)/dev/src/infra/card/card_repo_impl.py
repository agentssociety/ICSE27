from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.card.card_dto import CardCreate, CardUpdate, CardResponse


class SQLAlchemyCardRepository:
    def __init__(self, session: Session) -> None:
        from src.orm.card.card_orm import CardORM  # lazy import to avoid import-time error
        self._session = session
        self._CardORM = CardORM

    def get_by_id(self, item_id: int) -> Optional[CardResponse]:
        from src.orm.card.card_orm import CardORM  # lazy import to avoid import-time error
        row = self._session.get(self._CardORM, item_id)
        return CardResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[CardResponse]:
        from src.orm.card.card_orm import CardORM  # lazy import to avoid import-time error
        rows = self._session.query(self._CardORM).offset(skip).limit(limit).all()
        return [CardResponse.model_validate(r) for r in rows]

    def create(self, data: CardCreate) -> CardResponse:
        from src.orm.card.card_orm import CardORM  # lazy import to avoid import-time error
        row = self._CardORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return CardResponse.model_validate(row)

    def update(self, item_id: int, data: CardUpdate) -> Optional[CardResponse]:
        from src.orm.card.card_orm import CardORM  # lazy import to avoid import-time error
        row = self._session.get(self._CardORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return CardResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        from src.orm.card.card_orm import CardORM  # lazy import to avoid import-time error
        row = self._session.get(self._CardORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True