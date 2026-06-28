from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.blood_unit.blood_unit_dto import RecordBloodUnitRequest, BloodUnitResponse
from src.orm.blood_unit.blood_unit_orm import BloodUnitORM


class SQLAlchemyBloodUnitRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[BloodUnitResponse]:
        row = self._session.get(BloodUnitORM, item_id)
        return BloodUnitResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[BloodUnitResponse]:
        rows = self._session.query(BloodUnitORM).offset(skip).limit(limit).all()
        return [BloodUnitResponse.model_validate(r) for r in rows]

    def create(self, data: RecordBloodUnitRequest) -> BloodUnitResponse:
        row = BloodUnitORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return BloodUnitResponse.model_validate(row)

    def update(self, item_id: int, data: RecordBloodUnitRequest) -> Optional[BloodUnitResponse]:
        row = self._session.get(BloodUnitORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return BloodUnitResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(BloodUnitORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
