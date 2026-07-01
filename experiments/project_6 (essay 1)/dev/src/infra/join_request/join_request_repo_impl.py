from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.join_request.join_request_dto import JoinRequestCreate, JoinRequestUpdate, JoinRequestResponse
from src.orm.join_request.join_request_orm import JoinRequestORM


class SQLAlchemyJoinRequestRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[JoinRequestResponse]:
        row = self._session.get(JoinRequestORM, item_id)
        return JoinRequestResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[JoinRequestResponse]:
        rows = self._session.query(JoinRequestORM).offset(skip).limit(limit).all()
        return [JoinRequestResponse.model_validate(r) for r in rows]

    def create(self, data: JoinRequestCreate) -> JoinRequestResponse:
        row = JoinRequestORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return JoinRequestResponse.model_validate(row)

    def update(self, item_id: int, data: JoinRequestUpdate) -> Optional[JoinRequestResponse]:
        row = self._session.get(JoinRequestORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return JoinRequestResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(JoinRequestORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
