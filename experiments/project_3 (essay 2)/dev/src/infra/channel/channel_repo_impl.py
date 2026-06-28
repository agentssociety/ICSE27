from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.channel.channel_dto import ChannelCreate, ChannelUpdate, ChannelResponse
from src.orm.channel.channel_orm import ChannelORM


class SQLAlchemyChannelRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[ChannelResponse]:
        row = self._session.get(ChannelORM, item_id)
        return ChannelResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ChannelResponse]:
        rows = self._session.query(ChannelORM).offset(skip).limit(limit).all()
        return [ChannelResponse.model_validate(r) for r in rows]

    def create(self, data: ChannelCreate) -> ChannelResponse:
        row = ChannelORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return ChannelResponse.model_validate(row)

    def update(self, item_id: int, data: ChannelUpdate) -> Optional[ChannelResponse]:
        row = self._session.get(ChannelORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return ChannelResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(ChannelORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
