from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.message.message_dto import MessageCreate, MessageUpdate, MessageResponse
from src.orm.message.message_orm import MessageORM


class SQLAlchemyMessageRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[MessageResponse]:
        row = self._session.get(MessageORM, item_id)
        return MessageResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[MessageResponse]:
        rows = self._session.query(MessageORM).offset(skip).limit(limit).all()
        return [MessageResponse.model_validate(r) for r in rows]

    def create(self, data: MessageCreate) -> MessageResponse:
        row = MessageORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return MessageResponse.model_validate(row)

    def update(self, item_id: int, data: MessageUpdate) -> Optional[MessageResponse]:
        row = self._session.get(MessageORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return MessageResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(MessageORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
