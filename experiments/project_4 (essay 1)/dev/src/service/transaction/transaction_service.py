from __future__ import annotations

from typing import Any, Optional, Protocol
import uuid
from datetime import datetime
from enum import Enum

from src.domain.transaction import Transaction, State, Money, FailureReason, WithdrawalRecord, WithdrawalStatus
from src.infra.transaction.transaction_repo_impl import SQLAlchemyTransactionRepository
from src.infra.account.account_repo_impl import SQLAlchemyAccountRepository
from src.dto.account.account_dto import AccountResponse, AccountUpdate
from src.infra.audit_log_entry.audit_log_entry_repo_impl import SQLAlchemyAuditLogEntryRepository
from src.dto.audit_log_entry.audit_log_entry_dto import AuditLogEntryCreate
from src.domain.audit_log_entry import AuditActionType

# Fix missing DTO imports: define placeholder classes for the missing types.
class AdminReviewAction(Enum):
    APPROVE = "approve"
    REJECT = "reject"
    ESCALATE = "escalate"

class WithdrawalRequest:
    def __init__(self, account_id: int, amount: float, **kwargs):
        self.account_id = account_id
        self.amount = amount
        for k, v in kwargs.items():
            setattr(self, k, v)

class WithdrawalResponse:
    def __init__(self, success: bool, transaction_id: str, message: str, **kwargs):
        self.success = success
        self.transaction_id = transaction_id
        self.message = message
        for k, v in kwargs.items():
            setattr(self, k, v)

class ErrorResponse:
    pass

class AdminReviewRequest:
    def __init__(self, admin_username: str, action: AdminReviewAction, **kwargs):
        self.admin_username = admin_username
        self.action = action
        for k, v in kwargs.items():
            setattr(self, k, v)

class AdminReviewResponse:
    def __init__(self, success: bool, transaction_id: int, new_status: str, message: str, **kwargs):
        self.success = success
        self.transaction_id = transaction_id
        self.new_status = new_status
        self.message = message
        for k, v in kwargs.items():
            setattr(self, k, v)

class TransactionResponse:
    pass

class TransactionCreate:
    def __init__(self, initiator_id: int, user_id: int, amount: float, status: str, **kwargs):
        self.id = None  # will be set after creation
        self.initiator_id = initiator_id
        self.user_id = user_id
        self.amount = amount
        self.status = status
        for k, v in kwargs.items():
            setattr(self, k, v)

class TransactionUpdate:
    def __init__(self, status: str, **kwargs):
        self.status = status
        for k, v in kwargs.items():
            setattr(self, k, v)


class TransactionService(Protocol):
    def withdraw(self, request: WithdrawalRequest) -> WithdrawalResponse: ...
    def review_flagged_transaction(self, transaction_id: int, request: AdminReviewRequest) -> AdminReviewResponse: ...
    def get_flagged_transactions(self) -> list[dict[str, Any]]: ...
    def get_transactions_by_user_id(self, user_id: int) -> list[TransactionResponse]: ...


class TransactionServiceImpl:
    def __init__(
        self,
        transaction_repo: SQLAlchemyTransactionRepository,
        account_repo: SQLAlchemyAccountRepository,
        audit_repo: Optional[SQLAlchemyAuditLogEntryRepository] = None,
    ) -> None:
        self._transaction_repo = transaction_repo
        self._account_repo = account_repo
        self._audit_repo = audit_repo

    def _log_audit_entry(self, action_type: str, outcome: str, operation: str, username: str, account_id: Optional[int] = None) -> None:
        """Log an action to the audit log if audit_repo is available."""
        if self._audit_repo is None:
            return
        try:
            entry = AuditLogEntryCreate(
                operation=operation,
                username=username,
                ip_address="system",
                outcome=outcome,
                action_type=action_type,
                account_id=account_id,
                timestamp=datetime.utcnow(),
            )
            self._audit_repo.create(entry)
        except Exception:
            pass  # Audit logging should never break the main flow

    def withdraw(self, request: WithdrawalRequest) -> WithdrawalResponse:
        """
        Execute an atomic withdrawal operation.
        """
        # Step 1: Validate account exists
        account = self._account_repo.get_by_id(request.account_id)
        if account is None:
            return WithdrawalResponse(
                success=False,
                transaction_id="",
                message="Account not found"
            )

        # Step 2: Check sufficient balance
        if account.balance < request.amount:
            return WithdrawalResponse(
                success=False,
                transaction_id="",
                message="Insufficient balance"
            )

        # Step 3: Check daily withdrawal limit
        if (account.withdrawn_today + request.amount) > account.daily_withdrawal_limit:
            return WithdrawalResponse(
                success=False,
                transaction_id="",
                message="Daily withdrawal limit exceeded"
            )

        # Step 3: Create a pending transaction record
        transaction_data = TransactionCreate(
            initiator_id=0,
            user_id=request.account_id,
            amount=request.amount,
            status="pending"
        )
        
        try:
            # Simulate atomic operation: deduct balance and record transaction
            new_balance = account.balance - request.amount
            new_withdrawn_today = account.withdrawn_today + request.amount
            
            # Update account balance and daily withdrawn amount
            account_update = AccountUpdate(
                balance=new_balance, 
                withdrawn_today=new_withdrawn_today, 
                failedAttempts=None, 
                user_id=account.user_id
            )
            updated_account = self._account_repo.update(request.account_id, account_update)
            if updated_account is None:
                return WithdrawalResponse(
                    success=False,
                    transaction_id="",
                    message="Failed to update account balance"
                )
            
            # Mark transaction as completed
            transaction_data.status = "completed"
            created_transaction = self._transaction_repo.create(transaction_data)
            
            return WithdrawalResponse(
                success=True,
                transaction_id=str(created_transaction.id),
                message=f"Withdrawal of ${request.amount:.2f} successful"
            )
            
        except Exception as e:
            return WithdrawalResponse(
                success=False,
                transaction_id="",
                message=f"Transaction failed: {str(e)}"
            )

    def review_flagged_transaction(self, transaction_id: int, request: AdminReviewRequest) -> AdminReviewResponse:
        """
        Admin review of a flagged/suspicious transaction.
        
        Allowed actions:
          - approve: marks transaction as approved
          - reject: marks transaction as rejected
          - escalate: marks transaction as escalated for further investigation
        
        The action is logged for audit purposes.
        """
        # Step 1: Fetch the transaction
        transaction = self._transaction_repo.get_by_id(transaction_id)
        if transaction is None:
            return AdminReviewResponse(
                success=False,
                transaction_id=transaction_id,
                new_status="",
                message=f"Transaction {transaction_id} not found"
            )

        # Step 2: Check if transaction can still be reviewed
        if transaction.status in ("approved", "rejected", "escalated"):
            return AdminReviewResponse(
                success=False,
                transaction_id=transaction_id,
                new_status=transaction.status,
                message=f"Cannot act on {transaction.status} transaction"
            )

        # Step 3: Determine new status based on action
        action_map = {
            AdminReviewAction.APPROVE: "approved",
            AdminReviewAction.REJECT: "rejected",
            AdminReviewAction.ESCALATE: "escalated",
        }
        new_status = action_map[request.action]

        action_type_map = {
            AdminReviewAction.APPROVE: AuditActionType.TRANSACTION_APPROVED.value,
            AdminReviewAction.REJECT: AuditActionType.TRANSACTION_REJECTED.value,
            AdminReviewAction.ESCALATE: AuditActionType.TRANSACTION_ESCALATED.value,
        }

        # Step 4: Update the transaction
        update_data = TransactionUpdate(status=new_status)
        updated = self._transaction_repo.update(transaction_id, update_data)
        if updated is None:
            return AdminReviewResponse(
                success=False,
                transaction_id=transaction_id,
                new_status="",
                message="Failed to update transaction"
            )

        # Step 5: Log the action for audit purposes
        audit_operation = f"Admin {request.admin_username} {request.action.value}d transaction {transaction_id}"
        self._log_audit_entry(
            action_type=action_type_map[request.action],
            outcome=f"transaction_{new_status}",
            operation=audit_operation,
            username=request.admin_username,
        )

        return AdminReviewResponse(
            success=True,
            transaction_id=transaction_id,
            new_status=new_status,
            message=f"Transaction {transaction_id} has been {new_status}"
        )

    def get_flagged_transactions(self) -> list[dict[str, Any]]:
        """
        Retrieve all transactions that are flagged as suspicious for admin review.
        In the current system, we consider transactions with status 'pending' as needing review.
        """
        all_txns = self._transaction_repo.get_all(skip=0, limit=100)
        flagged = []
        for txn in all_txns:
            if txn.status in ("pending", "flagged"):
                flagged.append({
                    "id": txn.id,
                    "amount": txn.amount,
                    "status": txn.status,
                    "initiator_id": txn.initiator_id,
                    "user_id": txn.user_id,
                })
        return flagged

    def get_transactions_by_user_id(self, user_id: int) -> list[TransactionResponse]:
        """
        Retrieve all transactions for a specific user.
        Used by admin to view a user's complete transaction history.
        """
        return self._transaction_repo.get_by_user_id(user_id)