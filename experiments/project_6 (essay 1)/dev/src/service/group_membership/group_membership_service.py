from __future__ import annotations

from typing import Optional, Protocol, TYPE_CHECKING

from src.dto.group_membership.group_membership_dto import GroupMembershipCreate, GroupMembershipUpdate, GroupMembershipResponse

if TYPE_CHECKING:
    from src.infra.group_membership.group_membership_repo_impl import SQLAlchemyGroupMembershipRepository


class GroupMembershipService(Protocol):
    def get_by_id(self, item_id: int) -> Optional[GroupMembershipResponse]: ...
    def get_all(self, skip: int = 0, limit: int = 100) -> list[GroupMembershipResponse]: ...
    def create(self, data: GroupMembershipCreate) -> GroupMembershipResponse: ...
    def update(self, item_id: int, data: GroupMembershipUpdate) -> Optional[GroupMembershipResponse]: ...
    def delete(self, item_id: int) -> bool: ...


class GroupMembershipServiceImpl:
    def __init__(self, repo: SQLAlchemyGroupMembershipRepository) -> None:
        self._repo = repo

    def get_by_id(self, item_id: int) -> Optional[GroupMembershipResponse]:
        return self._repo.get_by_id(item_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[GroupMembershipResponse]:
        return self._repo.get_all(skip=skip, limit=limit)

    def create(self, data: GroupMembershipCreate) -> GroupMembershipResponse:
        return self._repo.create(data)

    def update(self, item_id: int, data: GroupMembershipUpdate) -> Optional[GroupMembershipResponse]:
        return self._repo.update(item_id, data)

    def delete(self, item_id: int) -> bool:
        return self._repo.delete(item_id)

