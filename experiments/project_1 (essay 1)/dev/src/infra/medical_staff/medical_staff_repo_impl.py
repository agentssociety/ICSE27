from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.medical_staff.medical_staff_dto import MedicalStaffCreate, MedicalStaffUpdate, MedicalStaffResponse
from src.orm.medical_staff.medical_staff_orm import MedicalStaffORM


class SQLAlchemyMedicalStaffRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[MedicalStaffResponse]:
        row = self._session.get(MedicalStaffORM, item_id)
        return MedicalStaffResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[MedicalStaffResponse]:
        rows = self._session.query(MedicalStaffORM).offset(skip).limit(limit).all()
        return [MedicalStaffResponse.model_validate(r) for r in rows]

    def create(self, data: MedicalStaffCreate) -> MedicalStaffResponse:
        row = MedicalStaffORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return MedicalStaffResponse.model_validate(row)

    def update(self, item_id: int, data: MedicalStaffUpdate) -> Optional[MedicalStaffResponse]:
        row = self._session.get(MedicalStaffORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return MedicalStaffResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(MedicalStaffORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
