from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.storage_state.storage_state_dto import StorageStateCreate, StorageStateUpdate, StorageStateResponse
from src.orm.storage_state.storage_state_orm import StorageStateORM


class SQLAlchemyStorageStateRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[StorageStateResponse]:
        row = self._session.get(StorageStateORM, item_id)
        return StorageStateResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[StorageStateResponse]:
        rows = self._session.query(StorageStateORM).offset(skip).limit(limit).all()
        return [StorageStateResponse.model_validate(r) for r in rows]

    def create(self, data: StorageStateCreate) -> StorageStateResponse:
        row = StorageStateORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return StorageStateResponse.model_validate(row)

    def update(self, item_id: int, data: StorageStateUpdate) -> Optional[StorageStateResponse]:
        row = self._session.get(StorageStateORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return StorageStateResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(StorageStateORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
