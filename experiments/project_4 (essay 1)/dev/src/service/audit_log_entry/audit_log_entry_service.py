from __future__ import annotations

from typing import Optional, Protocol
from datetime import datetime

from src.domain.audit_log_entry import AuditLogEntry, AuditActionType
from src.dto.audit_log_entry.audit_log_entry_dto import (
    AuditLogEntryCreate,
    AuditLogEntryResponse,
)


class AuditLogEntryService(Protocol):
    """Service protocol for audit log operations"""
    
    def log_authentication_attempt(
        self, username: str, ip_address: str, success: bool
    ) -> AuditLogEntry: ...
    
    def log_account_state_change(
        self, username: str, account_id: int, new_state: str
    ) -> AuditLogEntry: ...
    
    def get_recent_logs(
        self, skip: int = 0, limit: int = 100
    ) -> list[AuditLogEntryResponse]: ...


class AuditLogEntryServiceImpl:
    def __init__(
        self, repo: 'SQLAlchemyAuditLogEntryRepository'
    ) -> None:
        self._repo = repo

    def log_authentication_attempt(
        self, username: str, ip_address: str, success: bool
    ) -> AuditLogEntry:
        """Record an authentication attempt (success or failure)."""
        action_type = (
            AuditActionType.AUTHENTICATION_SUCCESS.value
            if success
            else AuditActionType.AUTHENTICATION_FAILURE.value
        )
        outcome = "success" if success else "failure"
        operation = f"Authentication attempt by {username} from {ip_address}: {outcome}"
        now = datetime.utcnow()
        
        dto = AuditLogEntryCreate(
            operation=operation,
            username=username,
            ip_address=ip_address,
            outcome=outcome,
            action_type=action_type,
            timestamp=now,
        )
        self._repo.create(dto)
        
        return AuditLogEntry(
            operation=operation,
            timestamp=now,
            username=username,
            ip_address=ip_address,
            outcome=outcome,
        )

    def log_account_state_change(
        self, username: str, account_id: int, new_state: str
    ) -> AuditLogEntry:
        """Record an account state change (lock/unlock)."""
        action_type = (
            AuditActionType.ACCOUNT_LOCKED.value
            if new_state == "locked"
            else AuditActionType.ACCOUNT_UNLOCKED.value
        )
        outcome = f"account_{new_state}"
        operation = f"Account {account_id} state changed to {new_state} by {username}"
        now = datetime.utcnow()
        
        dto = AuditLogEntryCreate(
            operation=operation,
            username=username,
            ip_address="system",
            outcome=outcome,
            action_type=action_type,
            account_id=account_id,
            timestamp=now,
        )
        self._repo.create(dto)
        
        return AuditLogEntry(
            operation=operation,
            timestamp=now,
            username=username,
            ip_address="system",
            outcome=outcome,
            account_id=account_id,
        )

    def get_recent_logs(
        self, skip: int = 0, limit: int = 100
    ) -> list[AuditLogEntryResponse]:
        """Retrieve recent audit log entries."""
        return self._repo.get_all(skip=skip, limit=limit)
