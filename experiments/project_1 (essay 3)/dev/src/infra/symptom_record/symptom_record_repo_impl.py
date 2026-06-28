from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.symptom_record.symptom_record_dto import SymptomRecordCreate, SymptomRecordUpdate, SymptomRecordResponse
from src.orm.symptom_record.symptom_record_orm import SymptomRecordORM


class SQLAlchemySymptomRecordRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[SymptomRecordResponse]:
        row = self._session.get(SymptomRecordORM, item_id)
        return SymptomRecordResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SymptomRecordResponse]:
        rows = self._session.query(SymptomRecordORM).offset(skip).limit(limit).all()
        return [SymptomRecordResponse.model_validate(r) for r in rows]

    def create(self, data: SymptomRecordCreate) -> SymptomRecordResponse:
        row = SymptomRecordORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return SymptomRecordResponse.model_validate(row)

    def update(self, item_id: int, data: SymptomRecordUpdate) -> Optional[SymptomRecordResponse]:
        row = self._session.get(SymptomRecordORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return SymptomRecordResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(SymptomRecordORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
