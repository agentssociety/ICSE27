from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.pin.pin_dto import PinCreateRequest, PinUpdateRequest, PinResponse
from src.orm.pin.pin_orm import PinORM

"""
Infra layer for the Pin domain class

Package: infra.pin
Layer: infra
Related tasks: #88
Requirement coverage:
- Card and PIN Authentication Requirement
"""


class SQLAlchemyPinRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: str) -> Optional[PinResponse]:
        row = self._session.get(PinORM, item_id)
        return PinResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[PinResponse]:
        rows = self._session.query(PinORM).offset(skip).limit(limit).all()
        return [PinResponse.model_validate(r) for r in rows]

    def create(self, data: PinCreateRequest) -> PinResponse:
        row = PinORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return PinResponse.model_validate(row)

    def update(self, item_id: str, data: PinUpdateRequest) -> Optional[PinResponse]:
        row = self._session.get(PinORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return PinResponse.model_validate(row)

    def delete(self, item_id: str) -> bool:
        row = self._session.get(PinORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
