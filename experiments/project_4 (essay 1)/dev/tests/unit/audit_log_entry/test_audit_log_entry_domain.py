from __future__ import annotations

import pytest
from datetime import datetime
from src.domain.audit_log_entry import AuditLogEntry, AuditLogEntryId, AuditActionType


class TestAuditLogEntryDomain:
    def test_audit_log_entry_creation(self) -> None:
        entry = AuditLogEntry(
            operation="Authentication attempt by testuser from 192.168.1.1: success",
            timestamp=datetime.utcnow(),
            username="testuser",
            ip_address="192.168.1.1",
            outcome="success",
        )
        assert entry.username == "testuser"
        assert entry.ip_address == "192.168.1.1"
        assert entry.outcome == "success"
        assert entry.action_type == AuditActionType.AUTHENTICATION_SUCCESS.value

    def test_audit_log_entry_with_custom_action_type(self) -> None:
        entry = AuditLogEntry(
            operation="Account 1 locked by admin",
            timestamp=datetime.utcnow(),
            username="admin",
            ip_address="system",
            outcome="account_locked",
            action_type=AuditActionType.ACCOUNT_LOCKED.value,
        )
        assert entry.action_type == AuditActionType.ACCOUNT_LOCKED.value

    def test_audit_log_entry_with_account_id(self) -> None:
        entry = AuditLogEntry(
            operation="Account 42 unlocked by admin",
            timestamp=datetime.utcnow(),
            username="admin",
            ip_address="system",
            outcome="account_unlocked",
            action_type=AuditActionType.ACCOUNT_UNLOCKED.value,
            account_id=42,
        )
        assert entry.account_id == 42

    def test_audit_log_entry_id_creation(self) -> None:
        entry_id = AuditLogEntryId()
        assert entry_id.value is not None
        assert isinstance(entry_id.value, str)
