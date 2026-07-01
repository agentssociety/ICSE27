from __future__ import annotations

from typing import Optional, Protocol, TYPE_CHECKING

from src.dto.message.message_dto import MessageCreate, MessageUpdate, MessageResponse

if TYPE_CHECKING:
    from src.infra.message.message_repo_impl import SQLAlchemyMessageRepository


class MessageService(Protocol):
    def get_by_id(self, item_id: int) -> Optional[MessageResponse]: ...
    def get_all(self, skip: int = 0, limit: int = 100) -> list[MessageResponse]: ...
    def create(self, data: MessageCreate) -> MessageResponse: ...
    def update(self, item_id: int, data: MessageUpdate) -> Optional[MessageResponse]: ...
    def delete(self, item_id: int) -> bool: ...


class MessageServiceImpl:
    def __init__(self, repo: SQLAlchemyMessageRepository) -> None:
        self._repo = repo

    def get_by_id(self, item_id: int) -> Optional[MessageResponse]:
        return self._repo.get_by_id(item_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[MessageResponse]:
        return self._repo.get_all(skip=skip, limit=limit)

    def create(self, data: MessageCreate) -> MessageResponse:
        return self._repo.create(data)

    def update(self, item_id: int, data: MessageUpdate) -> Optional[MessageResponse]:
        return self._repo.update(item_id, data)

    def delete(self, item_id: int) -> bool:
        return self._repo.delete(item_id)

