from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.chart_point.chart_point_dto import ChartPointCreate, ChartPointUpdate, ChartPointResponse
from src.orm.chart_point.chart_point_orm import ChartPointORM


class SQLAlchemyChartPointRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[ChartPointResponse]:
        row = self._session.get(ChartPointORM, item_id)
        return ChartPointResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ChartPointResponse]:
        rows = self._session.query(ChartPointORM).offset(skip).limit(limit).all()
        return [ChartPointResponse.model_validate(r) for r in rows]

    def create(self, data: ChartPointCreate) -> ChartPointResponse:
        row = ChartPointORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return ChartPointResponse.model_validate(row)

    def update(self, item_id: int, data: ChartPointUpdate) -> Optional[ChartPointResponse]:
        row = self._session.get(ChartPointORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return ChartPointResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(ChartPointORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
