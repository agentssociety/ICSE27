from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.patient_detail.patient_detail_dto import PatientDetailCreate, PatientDetailUpdate, PatientDetailResponse
from src.orm.patient_detail.patient_detail_orm import PatientDetailORM


class SQLAlchemyPatientDetailRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[PatientDetailResponse]:
        row = self._session.get(PatientDetailORM, item_id)
        return PatientDetailResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[PatientDetailResponse]:
        rows = self._session.query(PatientDetailORM).offset(skip).limit(limit).all()
        return [PatientDetailResponse.model_validate(r) for r in rows]

    def create(self, data: PatientDetailCreate) -> PatientDetailResponse:
        row = PatientDetailORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return PatientDetailResponse.model_validate(row)

    def update(self, item_id: int, data: PatientDetailUpdate) -> Optional[PatientDetailResponse]:
        row = self._session.get(PatientDetailORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return PatientDetailResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(PatientDetailORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
