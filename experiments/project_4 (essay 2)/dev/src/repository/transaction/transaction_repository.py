from __future__ import annotations

from typing import Any, Optional, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.transaction import Transaction

"""
Repository layer for the Transaction domain class

Package: repository.transaction
Layer: repository
Related tasks: #90, #92, #93
Requirement coverage:
- Enforce daily transaction limits
- Detect Suspicious Transaction Patterns
- Admin Interface for Flagged Transactions Review
"""

from src.dto.transaction.transaction_dto import TransactionCreateRequest, TransactionUpdateRequest, TransactionResponse


class FlaggedTransactionsReviewPage(Protocol):
    """Interface for paginated flagged transactions review."""
    def get_flagged_transactions(self, page: int, size: int) -> list[TransactionResponse]: ...


class TransactionsDatabase(Protocol):
    def get_transactions_by_account(self, account_id: str) -> list[TransactionResponse]: ...
    def get_recent_transactions(self, account_id: str, since: str) -> list[TransactionResponse]: ...


class AuthenticationAuthorizationService(Protocol):
    def authenticate(self, user_id: str, pin: str) -> bool: ...
    def authorize(self, user_id: str, permission: str) -> bool: ...


class Interface(Protocol):
    def get_by_id(self, item_id: str) -> Optional[TransactionResponse]: ...
    def get_all(self, skip: int = 0, limit: int = 100) -> list[TransactionResponse]: ...
    def create(self, data: TransactionCreateRequest) -> TransactionResponse: ...
    def update(self, item_id: str, data: TransactionUpdateRequest) -> Optional[TransactionResponse]: ...
    def delete(self, item_id: str) -> bool: ...
