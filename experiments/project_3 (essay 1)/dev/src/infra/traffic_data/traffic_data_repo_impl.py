from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from sqlalchemy.orm import Session

# Ensure project root is on sys.path for absolute imports
_project_root = Path(__file__).parent.parent.parent.resolve()
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from ...dto.traffic_data.traffic_data_dto import TrafficDataCreate, TrafficDataUpdate, TrafficDataResponse
from ...orm.traffic_data.traffic_data_orm import TrafficDataORM


class SQLAlchemyTrafficDataRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[TrafficDataResponse]:
        row = self._session.get(TrafficDataORM, item_id)
        return TrafficDataResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[TrafficDataResponse]:
        rows = self._session.query(TrafficDataORM).offset(skip).limit(limit).all()
        return [TrafficDataResponse.model_validate(r) for r in rows]

    def create(self, data: TrafficDataCreate) -> TrafficDataResponse:
        row = TrafficDataORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return TrafficDataResponse.model_validate(row)

    def update(self, item_id: int, data: TrafficDataUpdate) -> Optional[TrafficDataResponse]:
        row = self._session.get(TrafficDataORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return TrafficDataResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(TrafficDataORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True