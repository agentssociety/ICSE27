from __future__ import annotations

from typing import Optional, Protocol, TYPE_CHECKING

from src.dto.notification.notification_dto import NotificationCreate, NotificationUpdate, NotificationResponse

if TYPE_CHECKING:
    from src.infra.notification.notification_repo_impl import SQLAlchemyNotificationRepository


class NotificationService(Protocol):
    def get_by_id(self, item_id: int) -> Optional[NotificationResponse]: ...
    def get_all(self, skip: int = 0, limit: int = 100) -> list[NotificationResponse]: ...
    def create(self, data: NotificationCreate) -> NotificationResponse: ...
    def update(self, item_id: int, data: NotificationUpdate) -> Optional[NotificationResponse]: ...
    def delete(self, item_id: int) -> bool: ...


class NotificationServiceImpl:
    def __init__(self, repo: SQLAlchemyNotificationRepository) -> None:
        self._repo = repo

    def get_by_id(self, item_id: int) -> Optional[NotificationResponse]:
        return self._repo.get_by_id(item_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[NotificationResponse]:
        return self._repo.get_all(skip=skip, limit=limit)

    def create(self, data: NotificationCreate) -> NotificationResponse:
        return self._repo.create(data)

    def update(self, item_id: int, data: NotificationUpdate) -> Optional[NotificationResponse]:
        return self._repo.update(item_id, data)

    def delete(self, item_id: int) -> bool:
        return self._repo.delete(item_id)

