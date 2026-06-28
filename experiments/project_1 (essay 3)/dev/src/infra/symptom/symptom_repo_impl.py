from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.symptom.symptom_dto import SymptomCreate, SymptomUpdate, SymptomResponse
from src.orm.symptom.symptom_orm import SymptomORM


class SQLAlchemySymptomRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[SymptomResponse]:
        row = self._session.get(SymptomORM, item_id)
        return SymptomResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SymptomResponse]:
        rows = self._session.query(SymptomORM).offset(skip).limit(limit).all()
        return [SymptomResponse.model_validate(r) for r in rows]

    def create(self, data: SymptomCreate) -> SymptomResponse:
        row = SymptomORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return SymptomResponse.model_validate(row)

    def update(self, item_id: int, data: SymptomUpdate) -> Optional[SymptomResponse]:
        row = self._session.get(SymptomORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return SymptomResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(SymptomORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
