from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy.orm import Session

from src.dto.patient.patient_dto import PatientCreate, PatientUpdate, PatientResponse
from src.orm.patient.patient_orm import PatientORM


class SQLAlchemyPatientRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, patient_id: str) -> Optional[PatientResponse]:
        row = self._session.get(PatientORM, patient_id)
        return PatientResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[PatientResponse]:
        rows = self._session.query(PatientORM).offset(skip).limit(limit).all()
        return [PatientResponse.model_validate(r) for r in rows]

    def create(self, data: PatientCreate) -> PatientResponse:
        row = PatientORM(id=str(uuid.uuid4()), **data.model_dump())
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return PatientResponse.model_validate(row)

    def update(self, patient_id: str, data: PatientUpdate) -> Optional[PatientResponse]:
        row = self._session.get(PatientORM, patient_id)
        if row is None:
            return None
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(row, k, v)
        self._session.commit()
        self._session.refresh(row)
        return PatientResponse.model_validate(row)

    def delete(self, patient_id: str) -> bool:
        row = self._session.get(PatientORM, patient_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
