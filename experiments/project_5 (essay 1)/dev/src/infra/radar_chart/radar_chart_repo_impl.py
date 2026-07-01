from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.radar_chart.radar_chart_dto import RadarChartCreate, RadarChartUpdate, RadarChartResponse
from src.orm.radar_chart.radar_chart_orm import RadarChartORM


class SQLAlchemyRadarChartRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[RadarChartResponse]:
        row = self._session.get(RadarChartORM, item_id)
        return RadarChartResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[RadarChartResponse]:
        rows = self._session.query(RadarChartORM).offset(skip).limit(limit).all()
        return [RadarChartResponse.model_validate(r) for r in rows]

    def create(self, data: RadarChartCreate) -> RadarChartResponse:
        row = RadarChartORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return RadarChartResponse.model_validate(row)

    def update(self, item_id: int, data: RadarChartUpdate) -> Optional[RadarChartResponse]:
        row = self._session.get(RadarChartORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return RadarChartResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(RadarChartORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
