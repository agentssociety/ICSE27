from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.data_at_rest_encryption.data_at_rest_encryption_dto import DataAtRestEncryptionCreate, DataAtRestEncryptionUpdate, DataAtRestEncryptionResponse
from src.orm.data_at_rest_encryption.data_at_rest_encryption_orm import DataAtRestEncryptionORM


class SQLAlchemyDataAtRestEncryptionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[DataAtRestEncryptionResponse]:
        row = self._session.get(DataAtRestEncryptionORM, item_id)
        return DataAtRestEncryptionResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[DataAtRestEncryptionResponse]:
        rows = self._session.query(DataAtRestEncryptionORM).offset(skip).limit(limit).all()
        return [DataAtRestEncryptionResponse.model_validate(r) for r in rows]

    def create(self, data: DataAtRestEncryptionCreate) -> DataAtRestEncryptionResponse:
        row = DataAtRestEncryptionORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return DataAtRestEncryptionResponse.model_validate(row)

    def update(self, item_id: int, data: DataAtRestEncryptionUpdate) -> Optional[DataAtRestEncryptionResponse]:
        row = self._session.get(DataAtRestEncryptionORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return DataAtRestEncryptionResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(DataAtRestEncryptionORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True