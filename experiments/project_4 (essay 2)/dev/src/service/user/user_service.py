from __future__ import annotations

from typing import Any, Optional, Protocol

from src.dto.user.user_dto import UserCreateRequest, UserUpdateRequest, UserResponse

"""
Service layer for the User domain class

Package: service.user
Layer: service
Related tasks: #88, #89, #93, #94, #95
Requirement coverage:
- Card and PIN Authentication Requirement
- Account Lock After Three Consecutive Failed PIN Attempts
- Admin Interface for Flagged Transactions Review
- Manual Lock/Unlock User Accounts
- Audit Log Maintenance
"""


class UserService(Protocol):
    def create_user(self, data: UserCreateRequest) -> UserResponse: ...
    def get_user(self, user_id: str) -> Optional[UserResponse]: ...
    def get_all_users(self, skip: int = 0, limit: int = 100) -> list[UserResponse]: ...
    def update_user(self, user_id: str, data: UserUpdateRequest) -> Optional[UserResponse]: ...
    def delete_user(self, user_id: str) -> bool: ...


class UserServiceImpl:
    def __init__(self, repository: Any) -> None:
        self._repository = repository

    def create_user(self, data: UserCreateRequest) -> UserResponse:
        return self._repository.create(data)

    def get_user(self, user_id: str) -> Optional[UserResponse]:
        return self._repository.get_by_id(user_id)

    def get_all_users(self, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        return self._repository.get_all(skip=skip, limit=limit)

    def update_user(self, user_id: str, data: UserUpdateRequest) -> Optional[UserResponse]:
        return self._repository.update(user_id, data)

    def delete_user(self, user_id: str) -> bool:
        return self._repository.delete(user_id)
