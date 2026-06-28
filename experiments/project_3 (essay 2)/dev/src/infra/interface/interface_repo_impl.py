from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.interface.interface_dto import InterfaceCreate, InterfaceUpdate, InterfaceResponse
from src.orm.interface.interface_orm import InterfaceORM


class SQLAlchemyInterfaceRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[InterfaceResponse]:
        row = self._session.get(InterfaceORM, item_id)
        return InterfaceResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[InterfaceResponse]:
        rows = self._session.query(InterfaceORM).offset(skip).limit(limit).all()
        return [InterfaceResponse.model_validate(r) for r in rows]

    def create(self, data: InterfaceCreate) -> InterfaceResponse:
        row = InterfaceORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return InterfaceResponse.model_validate(row)

    def update(self, item_id: int, data: InterfaceUpdate) -> Optional[InterfaceResponse]:
        row = self._session.get(InterfaceORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return InterfaceResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(InterfaceORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
