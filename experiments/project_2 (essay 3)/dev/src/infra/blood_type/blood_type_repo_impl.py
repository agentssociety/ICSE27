from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.blood_type.blood_type_dto import BloodTypeCreate, BloodTypeUpdate, BloodTypeResponse
from src.orm.blood_type.blood_type_orm import BloodTypeORM


class SQLAlchemyBloodTypeRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[BloodTypeResponse]:
        row = self._session.get(BloodTypeORM, item_id)
        return BloodTypeResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[BloodTypeResponse]:
        rows = self._session.query(BloodTypeORM).offset(skip).limit(limit).all()
        return [BloodTypeResponse.model_validate(r) for r in rows]

    def create(self, data: BloodTypeCreate) -> BloodTypeResponse:
        row = BloodTypeORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return BloodTypeResponse.model_validate(row)

    def update(self, item_id: int, data: BloodTypeUpdate) -> Optional[BloodTypeResponse]:
        row = self._session.get(BloodTypeORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return BloodTypeResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(BloodTypeORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
