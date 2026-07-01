from __future__ import annotations

from typing import Optional, Protocol, TYPE_CHECKING

from src.dto.friendship.friendship_dto import FriendshipCreate, FriendshipUpdate, FriendshipResponse

if TYPE_CHECKING:
    from src.infra.friendship.friendship_repo_impl import SQLAlchemyFriendshipRepository


class FriendshipService(Protocol):
    def get_by_id(self, item_id: int) -> Optional[FriendshipResponse]: ...
    def get_all(self, skip: int = 0, limit: int = 100) -> list[FriendshipResponse]: ...
    def create(self, data: FriendshipCreate) -> FriendshipResponse: ...
    def update(self, item_id: int, data: FriendshipUpdate) -> Optional[FriendshipResponse]: ...
    def delete(self, item_id: int) -> bool: ...


class FriendshipServiceImpl:
    def __init__(self, repo: SQLAlchemyFriendshipRepository) -> None:
        self._repo = repo

    def get_by_id(self, item_id: int) -> Optional[FriendshipResponse]:
        return self._repo.get_by_id(item_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[FriendshipResponse]:
        return self._repo.get_all(skip=skip, limit=limit)

    def create(self, data: FriendshipCreate) -> FriendshipResponse:
        return self._repo.create(data)

    def update(self, item_id: int, data: FriendshipUpdate) -> Optional[FriendshipResponse]:
        return self._repo.update(item_id, data)

    def delete(self, item_id: int) -> bool:
        return self._repo.delete(item_id)

