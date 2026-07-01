from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.competency_trend_chart.competency_trend_chart_dto import CompetencyTrendChartCreate, CompetencyTrendChartUpdate, CompetencyTrendChartResponse
from src.orm.competency_trend_chart.competency_trend_chart_orm import CompetencyTrendChartORM


class SQLAlchemyCompetencyTrendChartRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[CompetencyTrendChartResponse]:
        row = self._session.get(CompetencyTrendChartORM, item_id)
        return CompetencyTrendChartResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[CompetencyTrendChartResponse]:
        rows = self._session.query(CompetencyTrendChartORM).offset(skip).limit(limit).all()
        return [CompetencyTrendChartResponse.model_validate(r) for r in rows]

    def create(self, data: CompetencyTrendChartCreate) -> CompetencyTrendChartResponse:
        row = CompetencyTrendChartORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return CompetencyTrendChartResponse.model_validate(row)

    def update(self, item_id: int, data: CompetencyTrendChartUpdate) -> Optional[CompetencyTrendChartResponse]:
        row = self._session.get(CompetencyTrendChartORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return CompetencyTrendChartResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(CompetencyTrendChartORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
