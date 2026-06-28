from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.symptom_data.symptom_data_dto import SymptomDataCreate, SymptomDataUpdate, SymptomDataResponse
from src.orm.symptom_data.symptom_data_orm import SymptomDataORM


class SQLAlchemySymptomDataRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[SymptomDataResponse]:
        row = self._session.get(SymptomDataORM, item_id)
        return SymptomDataResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SymptomDataResponse]:
        rows = self._session.query(SymptomDataORM).offset(skip).limit(limit).all()
        return [SymptomDataResponse.model_validate(r) for r in rows]

    def create(self, data: SymptomDataCreate) -> SymptomDataResponse:
        row = SymptomDataORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return SymptomDataResponse.model_validate(row)

    def update(self, item_id: int, data: SymptomDataUpdate) -> Optional[SymptomDataResponse]:
        row = self._session.get(SymptomDataORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return SymptomDataResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(SymptomDataORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True