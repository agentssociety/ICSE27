from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.queue_entry.queue_entry_dto import QueueEntryCreate, QueueEntryUpdate, QueueEntryResponse
from src.orm.queue_entry.queue_entry_orm import QueueEntryORM


class SQLAlchemyQueueEntryRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[QueueEntryResponse]:
        row = self._session.get(QueueEntryORM, item_id)
        if row is None:
            return None
        return QueueEntryResponse.model_validate(row)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[QueueEntryResponse]:
        rows = self._session.query(QueueEntryORM).offset(skip).limit(limit).all()
        return [QueueEntryResponse.model_validate(r) for r in rows]

    def create(self, data: QueueEntryCreate) -> QueueEntryResponse:
        row = QueueEntryORM(**data.model_dump())
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return QueueEntryResponse.model_validate(row)

    def update(self, item_id: int, data: QueueEntryUpdate) -> Optional[QueueEntryResponse]:
        row = self._session.get(QueueEntryORM, item_id)
        if row is None:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return QueueEntryResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(QueueEntryORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
