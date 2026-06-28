from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.state.state_dto import StateCreate, StateUpdate, StateResponse
from src.orm.state.state_orm import StateORM


class SQLAlchemyStateRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[StateResponse]:
        row = self._session.get(StateORM, item_id)
        return StateResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[StateResponse]:
        rows = self._session.query(StateORM).offset(skip).limit(limit).all()
        return [StateResponse.model_validate(r) for r in rows]

    def create(self, data: StateCreate) -> StateResponse:
        row = StateORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return StateResponse.model_validate(row)

    def update(self, item_id: int, data: StateUpdate) -> Optional[StateResponse]:
        row = self._session.get(StateORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return StateResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(StateORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
