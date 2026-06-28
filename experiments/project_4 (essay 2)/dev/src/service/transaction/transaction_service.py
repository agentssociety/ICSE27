from __future__ import annotations

from typing import Any, Optional, Protocol

from src.dto.transaction.transaction_dto import TransactionCreateRequest, TransactionUpdateRequest, TransactionResponse

"""
Service layer for the Transaction domain class

Package: service.transaction
Layer: service
Related tasks: #90, #92, #93
Requirement coverage:
- Enforce daily transaction limits
- Detect Suspicious Transaction Patterns
- Admin Interface for Flagged Transactions Review
"""


class TransactionService(Protocol):
    def create_transaction(self, data: TransactionCreateRequest) -> TransactionResponse: ...
    def get_transaction(self, transaction_id: str) -> Optional[TransactionResponse]: ...
    def get_all_transactions(self, skip: int = 0, limit: int = 100) -> list[TransactionResponse]: ...
    def update_transaction(self, transaction_id: str, data: TransactionUpdateRequest) -> Optional[TransactionResponse]: ...
    def delete_transaction(self, transaction_id: str) -> bool: ...


class TransactionServiceImpl:
    def __init__(self, repository: Any) -> None:
        self._repository = repository

    def create_transaction(self, data: TransactionCreateRequest) -> TransactionResponse:
        return self._repository.create(data)

    def get_transaction(self, transaction_id: str) -> Optional[TransactionResponse]:
        return self._repository.get_by_id(transaction_id)

    def get_all_transactions(self, skip: int = 0, limit: int = 100) -> list[TransactionResponse]:
        return self._repository.get_all(skip=skip, limit=limit)

    def update_transaction(self, transaction_id: str, data: TransactionUpdateRequest) -> Optional[TransactionResponse]:
        return self._repository.update(transaction_id, data)

    def delete_transaction(self, transaction_id: str) -> bool:
        return self._repository.delete(transaction_id)
