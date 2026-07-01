from __future__ import annotations

from typing import Optional, Protocol, TYPE_CHECKING

from src.dto.notification_preference.notification_preference_dto import NotificationPreferenceCreate, NotificationPreferenceUpdate, NotificationPreferenceResponse

if TYPE_CHECKING:
    from src.infra.notification_preference.notification_preference_repo_impl import SQLAlchemyNotificationPreferenceRepository


class NotificationPreferenceService(Protocol):
    def get_by_id(self, item_id: int) -> Optional[NotificationPreferenceResponse]: ...
    def get_all(self, skip: int = 0, limit: int = 100) -> list[NotificationPreferenceResponse]: ...
    def create(self, data: NotificationPreferenceCreate) -> NotificationPreferenceResponse: ...
    def update(self, item_id: int, data: NotificationPreferenceUpdate) -> Optional[NotificationPreferenceResponse]: ...
    def delete(self, item_id: int) -> bool: ...


class NotificationPreferenceServiceImpl:
    def __init__(self, repo: SQLAlchemyNotificationPreferenceRepository) -> None:
        self._repo = repo

    def get_by_id(self, item_id: int) -> Optional[NotificationPreferenceResponse]:
        return self._repo.get_by_id(item_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[NotificationPreferenceResponse]:
        return self._repo.get_all(skip=skip, limit=limit)

    def create(self, data: NotificationPreferenceCreate) -> NotificationPreferenceResponse:
        return self._repo.create(data)

    def update(self, item_id: int, data: NotificationPreferenceUpdate) -> Optional[NotificationPreferenceResponse]:
        return self._repo.update(item_id, data)

    def delete(self, item_id: int) -> bool:
        return self._repo.delete(item_id)

