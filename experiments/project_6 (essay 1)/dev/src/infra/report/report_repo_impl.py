from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.report.report_dto import ReportCreate, ReportUpdate, ReportResponse
from src.orm.report.report_orm import ReportORM


class SQLAlchemyReportRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[ReportResponse]:
        row = self._session.get(ReportORM, item_id)
        return ReportResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ReportResponse]:
        rows = self._session.query(ReportORM).offset(skip).limit(limit).all()
        return [ReportResponse.model_validate(r) for r in rows]

    def create(self, data: ReportCreate) -> ReportResponse:
        row = ReportORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return ReportResponse.model_validate(row)

    def update(self, item_id: int, data: ReportUpdate) -> Optional[ReportResponse]:
        row = self._session.get(ReportORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return ReportResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(ReportORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
