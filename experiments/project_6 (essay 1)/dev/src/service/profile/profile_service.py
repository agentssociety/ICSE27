from __future__ import annotations

from typing import Optional, Protocol, TYPE_CHECKING

from src.dto.profile.profile_dto import ProfileCreate, ProfileUpdate, ProfileResponse

if TYPE_CHECKING:
    from src.infra.profile.profile_repo_impl import SQLAlchemyProfileRepository


class ProfileService(Protocol):
    def get_by_id(self, item_id: int) -> Optional[ProfileResponse]: ...
    def get_all(self, skip: int = 0, limit: int = 100) -> list[ProfileResponse]: ...
    def create(self, data: ProfileCreate) -> ProfileResponse: ...
    def update(self, item_id: int, data: ProfileUpdate) -> Optional[ProfileResponse]: ...
    def delete(self, item_id: int) -> bool: ...


class ProfileServiceImpl:
    def __init__(self, repo: SQLAlchemyProfileRepository) -> None:
        self._repo = repo

    def get_by_id(self, item_id: int) -> Optional[ProfileResponse]:
        return self._repo.get_by_id(item_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ProfileResponse]:
        return self._repo.get_all(skip=skip, limit=limit)

    def create(self, data: ProfileCreate) -> ProfileResponse:
        return self._repo.create(data)

    def update(self, item_id: int, data: ProfileUpdate) -> Optional[ProfileResponse]:
        return self._repo.update(item_id, data)

    def delete(self, item_id: int) -> bool:
        return self._repo.delete(item_id)

