from __future__ import annotations

from typing import Optional
from sqlalchemy.orm import Session

from src.dto.user.user_dto import UserCreateRequest, UserUpdateRequest, UserResponse, UserListResponse
from src.infra.user.user_repo_impl import SQLAlchemyUserRepository
from src.domain.user.User import User, UserRole, UserStatus


class UserService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._repo = SQLAlchemyUserRepository(session)

    def create_user(self, data: UserCreateRequest) -> UserResponse:
        return self._repo.create(data)

    def get_user(self, user_id: str) -> Optional[UserResponse]:
        return self._repo.get_by_id(user_id)

    def list_users(self, skip: int = 0, limit: int = 100) -> UserListResponse:
        items = self._repo.get_all(skip=skip, limit=limit)
        total = self._repo.count()
        return UserListResponse(items=items, total=total)

    def update_user(self, user_id: str, data: UserUpdateRequest) -> Optional[UserResponse]:
        return self._repo.update(user_id, data)

    def deactivate_user(self, user_id: str) -> Optional[UserResponse]:
        return self._repo.deactivate(user_id)

    def activate_user(self, user_id: str) -> Optional[UserResponse]:
        return self._repo.activate(user_id)

    def delete_user(self, user_id: str) -> bool:
        return self._repo.delete(user_id)
