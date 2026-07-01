from __future__ import annotations

from typing import Optional, Protocol, TYPE_CHECKING

from src.dto.group.group_dto import GroupCreate, GroupUpdate, GroupResponse

if TYPE_CHECKING:
    from src.infra.group.group_repo_impl import SQLAlchemyGroupRepository


class GroupService(Protocol):
    def get_by_id(self, item_id: int) -> Optional[GroupResponse]: ...
    def get_all(self, skip: int = 0, limit: int = 100) -> list[GroupResponse]: ...
    def create(self, data: GroupCreate) -> GroupResponse: ...
    def update(self, item_id: int, data: GroupUpdate) -> Optional[GroupResponse]: ...
    def delete(self, item_id: int) -> bool: ...


class GroupServiceImpl:
    def __init__(self, repo: SQLAlchemyGroupRepository) -> None:
        self._repo = repo

    def get_by_id(self, item_id: int) -> Optional[GroupResponse]:
        return self._repo.get_by_id(item_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[GroupResponse]:
        return self._repo.get_all(skip=skip, limit=limit)

    def create(self, data: GroupCreate) -> GroupResponse:
        return self._repo.create(data)

    def update(self, item_id: int, data: GroupUpdate) -> Optional[GroupResponse]:
        return self._repo.update(item_id, data)

    def delete(self, item_id: int) -> bool:
        return self._repo.delete(item_id)

