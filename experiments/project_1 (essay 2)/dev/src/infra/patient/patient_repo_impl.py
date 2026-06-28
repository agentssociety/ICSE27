from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.patient.patient_dto import PatientCreate, PatientUpdate, PatientResponse
from src.orm.patient.patient_orm import PatientORM


class SQLAlchemyPatientRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[PatientResponse]:
        row = self._session.get(PatientORM, item_id)
        if row is None:
            return None
        return PatientResponse.model_validate(row)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[PatientResponse]:
        rows = self._session.query(PatientORM).offset(skip).limit(limit).all()
        return [PatientResponse.model_validate(r) for r in rows]

    def create(self, data: PatientCreate) -> PatientResponse:
        row = PatientORM(**data.model_dump())
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return PatientResponse.model_validate(row)

    def update(self, item_id: int, data: PatientUpdate) -> Optional[PatientResponse]:
        row = self._session.get(PatientORM, item_id)
        if row is None:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return PatientResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(PatientORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
