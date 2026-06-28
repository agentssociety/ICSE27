from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.patient_queue.patient_queue_dto import PatientQueueCreate, PatientQueueUpdate, PatientQueueResponse
from src.orm.patient_queue.patient_queue_orm import PatientQueueORM


class SQLAlchemyPatientQueueRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[PatientQueueResponse]:
        row = self._session.get(PatientQueueORM, item_id)
        return PatientQueueResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[PatientQueueResponse]:
        rows = self._session.query(PatientQueueORM).offset(skip).limit(limit).all()
        return [PatientQueueResponse.model_validate(r) for r in rows]

    def create(self, data: PatientQueueCreate) -> PatientQueueResponse:
        row = PatientQueueORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return PatientQueueResponse.model_validate(row)

    def update(self, item_id: int, data: PatientQueueUpdate) -> Optional[PatientQueueResponse]:
        row = self._session.get(PatientQueueORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return PatientQueueResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(PatientQueueORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
