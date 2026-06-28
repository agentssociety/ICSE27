from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.symptom_resource.symptom_resource_dto import SymptomResourceCreate, SymptomResourceUpdate, SymptomResourceResponse
from src.orm.symptom_resource.symptom_resource_orm import SymptomResourceORM


class SQLAlchemySymptomResourceRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[SymptomResourceResponse]:
        row = self._session.get(SymptomResourceORM, item_id)
        return SymptomResourceResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SymptomResourceResponse]:
        rows = self._session.query(SymptomResourceORM).offset(skip).limit(limit).all()
        return [SymptomResourceResponse.model_validate(r) for r in rows]

    def create(self, data: SymptomResourceCreate) -> SymptomResourceResponse:
        row = SymptomResourceORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return SymptomResourceResponse.model_validate(row)

    def update(self, item_id: int, data: SymptomResourceUpdate) -> Optional[SymptomResourceResponse]:
        row = self._session.get(SymptomResourceORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return SymptomResourceResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(SymptomResourceORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
