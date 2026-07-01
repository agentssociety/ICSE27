from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.role.role_dto import RoleCreate, RoleUpdate, RoleResponse
from src.orm.role.role_orm import RoleORM


class SQLAlchemyRoleRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[RoleResponse]:
        row = self._session.get(RoleORM, item_id)
        return RoleResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[RoleResponse]:
        rows = self._session.query(RoleORM).offset(skip).limit(limit).all()
        return [RoleResponse.model_validate(r) for r in rows]

    def create(self, data: RoleCreate) -> RoleResponse:
        row = RoleORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return RoleResponse.model_validate(row)

    def update(self, item_id: int, data: RoleUpdate) -> Optional[RoleResponse]:
        row = self._session.get(RoleORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return RoleResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(RoleORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
