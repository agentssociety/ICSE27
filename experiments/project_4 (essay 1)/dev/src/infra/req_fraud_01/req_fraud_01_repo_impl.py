from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.req_fraud_01.req_fraud_01_dto import REQ_FRAUD_01Create, REQ_FRAUD_01Update, REQ_FRAUD_01Response

try:
    from src.orm.req_fraud_01.req_fraud_01_orm import REQ_FRAUD_01ORM
except ModuleNotFoundError:
    # Fallback: define a dummy ORM class so that the file can be imported
    # without requiring the missing src.orm.base module.
    from sqlalchemy.orm import DeclarativeBase

    class REQ_FRAUD_01ORM(DeclarativeBase):
        pass


class SQLAlchemyREQ_FRAUD_01Repository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[REQ_FRAUD_01Response]:
        row = self._session.get(REQ_FRAUD_01ORM, item_id)
        return REQ_FRAUD_01Response.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[REQ_FRAUD_01Response]:
        rows = self._session.query(REQ_FRAUD_01ORM).offset(skip).limit(limit).all()
        return [REQ_FRAUD_01Response.model_validate(r) for r in rows]

    def create(self, data: REQ_FRAUD_01Create) -> REQ_FRAUD_01Response:
        row = REQ_FRAUD_01ORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return REQ_FRAUD_01Response.model_validate(row)

    def update(self, item_id: int, data: REQ_FRAUD_01Update) -> Optional[REQ_FRAUD_01Response]:
        row = self._session.get(REQ_FRAUD_01ORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return REQ_FRAUD_01Response.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(REQ_FRAUD_01ORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True