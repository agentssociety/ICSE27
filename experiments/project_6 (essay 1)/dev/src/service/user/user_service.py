from __future__ import annotations

from typing import Optional, Protocol, TYPE_CHECKING
import hashlib

from src.dto.user.user_dto import UserCreate, UserUpdate, UserResponse, RegistrationRequest, RegistrationResponse, LoginRequest, LoginResponse

if TYPE_CHECKING:
    from src.infra.user.user_repo_impl import SQLAlchemyUserRepository


class UserService(Protocol):
    def register(self, request: RegistrationRequest) -> RegistrationResponse: ...
    def get_by_id(self, user_id: int) -> Optional[UserResponse]: ...
    def get_by_email(self, email: str) -> Optional[UserResponse]: ...
    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserResponse]: ...
    def update(self, user_id: int, data: UserUpdate) -> Optional[UserResponse]: ...
    def delete(self, user_id: int) -> bool: ...
    def soft_delete(self, user_id: int) -> Optional[UserResponse]: ...
    def recover(self, user_id: int) -> Optional[UserResponse]: ...


class UserServiceImpl:
    def __init__(self, repo: SQLAlchemyUserRepository) -> None:
        self._repo = repo

    def login(self, request: LoginRequest) -> LoginResponse:
        row = self._repo.find_orm_by_email(request.email)
        if row is None:
            raise ValueError("Invalid email or password")
        hashed = hashlib.sha256(request.password.encode()).hexdigest()
        if row.passwordHash != hashed:
            raise ValueError("Invalid email or password")
        return LoginResponse(userId=row.id, email=row.email, name=row.name, message="Login successful")

    def register(self, request: RegistrationRequest) -> RegistrationResponse:
        existing = self._repo.find_by_email(request.email)
        if existing:
            raise ValueError(f"Email {request.email} already registered")
        hashed_pw = hashlib.sha256(request.password.encode()).hexdigest()
        user_data = UserCreate(
            email=request.email,
            password=hashed_pw,
            name=request.name
        )
        created = self._repo.create(user_data)
        return RegistrationResponse(
            userId=created.id,
            email=created.email,
            message="Account created. Please check your email to confirm."
        )

    def get_by_id(self, user_id: int) -> Optional[UserResponse]:
        return self._repo.get_by_id(user_id)

    def get_by_email(self, email: str) -> Optional[UserResponse]:
        return self._repo.find_by_email(email)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        return self._repo.get_all(skip=skip, limit=limit)

    def update(self, user_id: int, data: UserUpdate) -> Optional[UserResponse]:
        return self._repo.update(user_id, data)

    def delete(self, user_id: int) -> bool:
        return self._repo.delete(user_id)

    def soft_delete(self, user_id: int) -> Optional[UserResponse]:
        return self._repo.update(user_id, UserUpdate(accountStatus="deleted"))

    def recover(self, user_id: int) -> Optional[UserResponse]:
        return self._repo.update(user_id, UserUpdate(accountStatus="active"))
