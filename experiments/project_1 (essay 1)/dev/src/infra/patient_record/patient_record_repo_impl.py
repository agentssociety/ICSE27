from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.patient_record.patient_record_dto import PatientRecordCreate, PatientRecordUpdate, PatientRecordResponse
from src.orm.patient_record.patient_record_orm import PatientRecordORM


class SQLAlchemyPatientRecordRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[PatientRecordResponse]:
        row = self._session.get(PatientRecordORM, item_id)
        return PatientRecordResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[PatientRecordResponse]:
        rows = self._session.query(PatientRecordORM).offset(skip).limit(limit).all()
        return [PatientRecordResponse.model_validate(r) for r in rows]

    def create(self, data: PatientRecordCreate) -> PatientRecordResponse:
        row = PatientRecordORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return PatientRecordResponse.model_validate(row)

    def update(self, item_id: int, data: PatientRecordUpdate) -> Optional[PatientRecordResponse]:
        row = self._session.get(PatientRecordORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return PatientRecordResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(PatientRecordORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
