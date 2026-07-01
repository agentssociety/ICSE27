from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.competency.competency_dto import CompetencyCreate, CompetencyUpdate, CompetencyResponse
from src.orm.competency.competency_orm import CompetencyORM


class SQLAlchemyCompetencyRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[CompetencyResponse]:
        row = self._session.get(CompetencyORM, item_id)
        return CompetencyResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[CompetencyResponse]:
        rows = self._session.query(CompetencyORM).offset(skip).limit(limit).all()
        return [CompetencyResponse.model_validate(r) for r in rows]

    def create(self, data: CompetencyCreate) -> CompetencyResponse:
        row = CompetencyORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return CompetencyResponse.model_validate(row)

    def update(self, item_id: int, data: CompetencyUpdate) -> Optional[CompetencyResponse]:
        row = self._session.get(CompetencyORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return CompetencyResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(CompetencyORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
