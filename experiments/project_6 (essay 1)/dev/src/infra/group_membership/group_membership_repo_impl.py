from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.group_membership.group_membership_dto import GroupMembershipCreate, GroupMembershipUpdate, GroupMembershipResponse
from src.orm.group_membership.group_membership_orm import GroupMembershipORM


class SQLAlchemyGroupMembershipRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[GroupMembershipResponse]:
        row = self._session.get(GroupMembershipORM, item_id)
        return GroupMembershipResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[GroupMembershipResponse]:
        rows = self._session.query(GroupMembershipORM).offset(skip).limit(limit).all()
        return [GroupMembershipResponse.model_validate(r) for r in rows]

    def create(self, data: GroupMembershipCreate) -> GroupMembershipResponse:
        row = GroupMembershipORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return GroupMembershipResponse.model_validate(row)

    def update(self, item_id: int, data: GroupMembershipUpdate) -> Optional[GroupMembershipResponse]:
        row = self._session.get(GroupMembershipORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return GroupMembershipResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(GroupMembershipORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
