from __future__ import annotations

from typing import Optional

from sqlalchemy import Column, Integer
from sqlalchemy.orm import Session, declarative_base

# Local stub to avoid missing module dependency
Base = declarative_base()


class PINORM(Base):
    __tablename__ = "pins"
    id = Column(Integer, primary_key=True)


class SQLAlchemyPINRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[PINResponse]:
        row = self._session.get(PINORM, item_id)
        return PINResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[PINResponse]:
        rows = self._session.query(PINORM).offset(skip).limit(limit).all()
        return [PINResponse.model_validate(r) for r in rows]

    def create(self, data: PINCreate) -> PINResponse:
        row = PINORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return PINResponse.model_validate(row)

    def update(self, item_id: int, data: PINUpdate) -> Optional[PINResponse]:
        row = self._session.get(PINORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return PINResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(PINORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True