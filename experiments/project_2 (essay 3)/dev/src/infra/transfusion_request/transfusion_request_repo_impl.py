from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.transfusion_request.transfusion_request_dto import TransfusionRequestCreate, TransfusionRequestUpdate, TransfusionRequestResponse
from src.orm.transfusion_request.transfusion_request_orm import TransfusionRequestORM


class SQLAlchemyTransfusionRequestRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[TransfusionRequestResponse]:
        row = self._session.get(TransfusionRequestORM, item_id)
        return TransfusionRequestResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[TransfusionRequestResponse]:
        rows = self._session.query(TransfusionRequestORM).offset(skip).limit(limit).all()
        return [TransfusionRequestResponse.model_validate(r) for r in rows]

    def create(self, data: TransfusionRequestCreate) -> TransfusionRequestResponse:
        row = TransfusionRequestORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return TransfusionRequestResponse.model_validate(row)

    def update(self, item_id: int, data: TransfusionRequestUpdate) -> Optional[TransfusionRequestResponse]:
        row = self._session.get(TransfusionRequestORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return TransfusionRequestResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(TransfusionRequestORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
