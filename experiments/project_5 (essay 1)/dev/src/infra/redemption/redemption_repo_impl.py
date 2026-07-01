from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.redemption.redemption_dto import RedemptionCreate, RedemptionUpdate, RedemptionResponse
from src.orm.redemption.redemption_orm import RedemptionORM


class SQLAlchemyRedemptionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[RedemptionResponse]:
        row = self._session.get(RedemptionORM, item_id)
        return RedemptionResponse.model_validate(row) if row else None

    def get_by_student_id(self, student_id: int) -> list[RedemptionResponse]:
        rows = self._session.query(RedemptionORM).filter(RedemptionORM.student_id == student_id).all()
        return [RedemptionResponse.model_validate(r) for r in rows]

    def get_all(self, skip: int = 0, limit: int = 100) -> list[RedemptionResponse]:
        rows = self._session.query(RedemptionORM).offset(skip).limit(limit).all()
        return [RedemptionResponse.model_validate(r) for r in rows]

    def create(self, data: RedemptionCreate) -> RedemptionResponse:
        row = RedemptionORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return RedemptionResponse.model_validate(row)

    def update(self, item_id: int, data: RedemptionUpdate) -> Optional[RedemptionResponse]:
        row = self._session.get(RedemptionORM, item_id)
        if row is None:
            return None
        self._session.commit()
        self._session.refresh(row)
        return RedemptionResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(RedemptionORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
