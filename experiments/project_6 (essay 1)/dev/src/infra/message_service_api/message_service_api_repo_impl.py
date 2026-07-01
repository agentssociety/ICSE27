from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.message_service_api.message_service_api_dto import Message_Service_APICreate, Message_Service_APIUpdate, Message_Service_APIResponse
from src.orm.message_service_api.message_service_api_orm import Message_Service_APIORM


class SQLAlchemyMessage_Service_APIRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[Message_Service_APIResponse]:
        row = self._session.get(Message_Service_APIORM, item_id)
        return Message_Service_APIResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Message_Service_APIResponse]:
        rows = self._session.query(Message_Service_APIORM).offset(skip).limit(limit).all()
        return [Message_Service_APIResponse.model_validate(r) for r in rows]

    def create(self, data: Message_Service_APICreate) -> Message_Service_APIResponse:
        row = Message_Service_APIORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return Message_Service_APIResponse.model_validate(row)

    def update(self, item_id: int, data: Message_Service_APIUpdate) -> Optional[Message_Service_APIResponse]:
        row = self._session.get(Message_Service_APIORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return Message_Service_APIResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(Message_Service_APIORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
