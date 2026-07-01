from __future__ import annotations

from typing import Optional, Protocol, TYPE_CHECKING

from src.dto.verified_badge.verified_badge_dto import VerifiedBadgeCreate, VerifiedBadgeUpdate, VerifiedBadgeResponse

if TYPE_CHECKING:
    from src.infra.verified_badge.verified_badge_repo_impl import SQLAlchemyVerifiedBadgeRepository


class VerifiedBadgeService(Protocol):
    def get_by_id(self, item_id: int) -> Optional[VerifiedBadgeResponse]: ...
    def get_all(self, skip: int = 0, limit: int = 100) -> list[VerifiedBadgeResponse]: ...
    def create(self, data: VerifiedBadgeCreate) -> VerifiedBadgeResponse: ...
    def update(self, item_id: int, data: VerifiedBadgeUpdate) -> Optional[VerifiedBadgeResponse]: ...
    def delete(self, item_id: int) -> bool: ...

    def grant_badge(self, user_id: str, admin_id: str) -> object: ...
    def revoke_badge(self, badge_id: int) -> bool: ...


class VerifiedBadgeServiceImpl:
    def __init__(self, repo: SQLAlchemyVerifiedBadgeRepository) -> None:
        self._repo = repo

    def get_by_id(self, item_id: int) -> Optional[VerifiedBadgeResponse]:
        return self._repo.get_by_id(item_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[VerifiedBadgeResponse]:
        return self._repo.get_all(skip=skip, limit=limit)

    def create(self, data: VerifiedBadgeCreate) -> VerifiedBadgeResponse:
        return self._repo.create(data)

    def update(self, item_id: int, data: VerifiedBadgeUpdate) -> Optional[VerifiedBadgeResponse]:
        return self._repo.update(item_id, data)

    def delete(self, item_id: int) -> bool:
        return self._repo.delete(item_id)

