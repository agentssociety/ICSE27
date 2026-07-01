from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.group.group_dto import GroupCreate, GroupUpdate, GroupResponse
from src.orm.group.group_orm import GroupORM


class SQLAlchemyGroupRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[GroupResponse]:
        row = self._session.get(GroupORM, item_id)
        return GroupResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[GroupResponse]:
        rows = self._session.query(GroupORM).offset(skip).limit(limit).all()
        return [GroupResponse.model_validate(r) for r in rows]

    def create(self, data: GroupCreate) -> GroupResponse:
        row = GroupORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return GroupResponse.model_validate(row)

    def update(self, item_id: int, data: GroupUpdate) -> Optional[GroupResponse]:
        row = self._session.get(GroupORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return GroupResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(GroupORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
