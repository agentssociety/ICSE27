from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.reward_store.reward_store_dto import RewardStoreCreate, RewardStoreUpdate, RewardStoreResponse
from src.orm.reward_store.reward_store_orm import RewardStoreORM


class SQLAlchemyRewardStoreRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[RewardStoreResponse]:
        row = self._session.get(RewardStoreORM, item_id)
        return RewardStoreResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[RewardStoreResponse]:
        rows = self._session.query(RewardStoreORM).offset(skip).limit(limit).all()
        return [RewardStoreResponse.model_validate(r) for r in rows]

    def create(self, data: RewardStoreCreate) -> RewardStoreResponse:
        row = RewardStoreORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return RewardStoreResponse.model_validate(row)

    def update(self, item_id: int, data: RewardStoreUpdate) -> Optional[RewardStoreResponse]:
        row = self._session.get(RewardStoreORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return RewardStoreResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(RewardStoreORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
