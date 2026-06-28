from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.permission.permission_dto import PermissionCreate, PermissionUpdate, PermissionResponse
from src.orm.permission.permission_orm import PermissionORM


class SQLAlchemyPermissionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[PermissionResponse]:
        row = self._session.get(PermissionORM, item_id)
        return PermissionResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[PermissionResponse]:
        rows = self._session.query(PermissionORM).offset(skip).limit(limit).all()
        return [PermissionResponse.model_validate(r) for r in rows]

    def create(self, data: PermissionCreate) -> PermissionResponse:
        row = PermissionORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return PermissionResponse.model_validate(row)

    def update(self, item_id: int, data: PermissionUpdate) -> Optional[PermissionResponse]:
        row = self._session.get(PermissionORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return PermissionResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(PermissionORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
