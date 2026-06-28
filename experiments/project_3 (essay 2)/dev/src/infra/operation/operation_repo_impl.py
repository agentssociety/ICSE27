from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.operation.operation_dto import OperationCreate, OperationUpdate, OperationResponse
from src.orm.operation.operation_orm import OperationORM


class SQLAlchemyOperationRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[OperationResponse]:
        row = self._session.get(OperationORM, item_id)
        return OperationResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[OperationResponse]:
        rows = self._session.query(OperationORM).offset(skip).limit(limit).all()
        return [OperationResponse.model_validate(r) for r in rows]

    def create(self, data: OperationCreate) -> OperationResponse:
        row = OperationORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return OperationResponse.model_validate(row)

    def update(self, item_id: int, data: OperationUpdate) -> Optional[OperationResponse]:
        row = self._session.get(OperationORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return OperationResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(OperationORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
