from __future__ import annotations

from typing import Any, Optional, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.user import Bool, IfaceKind

"""
Repository layer for the User domain class

Package: repository.user
Layer: repository
Related tasks: #88, #89, #93, #94, #95
Requirement coverage:
- Card and PIN Authentication Requirement
- Account Lock After Three Consecutive Failed PIN Attempts
- Admin Interface for Flagged Transactions Review
- Manual Lock/Unlock User Accounts
- Audit Log Maintenance
"""

from src.dto.user.user_dto import UserCreateRequest, UserUpdateRequest, UserResponse


class Interface(Protocol):
    def get_by_id(self, item_id: str) -> Optional[UserResponse]: ...
    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserResponse]: ...
    def create(self, data: UserCreateRequest) -> UserResponse: ...
    def update(self, item_id: str, data: UserUpdateRequest) -> Optional[UserResponse]: ...
    def delete(self, item_id: str) -> bool: ...


class CardReader(Protocol):
    def readCard(self, cardData: Any) -> None:
        ...


class PINVerificationService(Protocol):
    def verify_pin(self, user_id: str, pin: str) -> bool:
        ...
