from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.competency_breakdown.competency_breakdown_dto import CompetencyBreakdownCreate, CompetencyBreakdownUpdate, CompetencyBreakdownResponse
from src.orm.competency_breakdown.competency_breakdown_orm import CompetencyBreakdownORM


class SQLAlchemyCompetencyBreakdownRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[CompetencyBreakdownResponse]:
        row = self._session.get(CompetencyBreakdownORM, item_id)
        return CompetencyBreakdownResponse.model_validate(row) if row else None

    def get_by_session(self, exam_session_id: int) -> list[CompetencyBreakdownResponse]:
        rows = self._session.query(CompetencyBreakdownORM).filter(CompetencyBreakdownORM.exam_session_id == exam_session_id).all()
        return [CompetencyBreakdownResponse.model_validate(r) for r in rows]

    def get_all(self, skip: int = 0, limit: int = 100) -> list[CompetencyBreakdownResponse]:
        rows = self._session.query(CompetencyBreakdownORM).offset(skip).limit(limit).all()
        return [CompetencyBreakdownResponse.model_validate(r) for r in rows]

    def create(self, data: CompetencyBreakdownCreate) -> CompetencyBreakdownResponse:
        row = CompetencyBreakdownORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return CompetencyBreakdownResponse.model_validate(row)

    def update(self, item_id: int, data: CompetencyBreakdownUpdate) -> Optional[CompetencyBreakdownResponse]:
        row = self._session.get(CompetencyBreakdownORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return CompetencyBreakdownResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(CompetencyBreakdownORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
