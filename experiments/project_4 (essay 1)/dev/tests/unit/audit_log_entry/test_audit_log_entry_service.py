from __future__ import annotations

import pytest
from unittest.mock import MagicMock
from datetime import datetime
from src.service.audit_log_entry.audit_log_entry_service import (
    AuditLogEntryServiceImpl,
)


class TestAuditLogEntryService:
    def test_log_authentication_success(self) -> None:
        mock_repo = MagicMock()
        mock_repo.create.return_value = MagicMock()
        service = AuditLogEntryServiceImpl(mock_repo)
        
        entry = service.log_authentication_attempt(
            username="testuser",
            ip_address="192.168.1.1",
            success=True,
        )
        
        assert entry.username == "testuser"
        assert entry.ip_address == "192.168.1.1"
        assert entry.outcome == "success"
        assert mock_repo.create.called

    def test_log_authentication_failure(self) -> None:
        mock_repo = MagicMock()
        mock_repo.create.return_value = MagicMock()
        service = AuditLogEntryServiceImpl(mock_repo)
        
        entry = service.log_authentication_attempt(
            username="testuser",
            ip_address="192.168.1.1",
            success=False,
        )
        
        assert entry.username == "testuser"
        assert entry.outcome == "failure"
        assert mock_repo.create.called

    def test_log_account_locked(self) -> None:
        mock_repo = MagicMock()
        mock_repo.create.return_value = MagicMock()
        service = AuditLogEntryServiceImpl(mock_repo)
        
        entry = service.log_account_state_change(
            username="admin",
            account_id=1,
            new_state="locked",
        )
        
        assert entry.account_id == 1
        assert entry.outcome == "account_locked"
        assert mock_repo.create.called

    def test_log_account_unlocked(self) -> None:
        mock_repo = MagicMock()
        mock_repo.create.return_value = MagicMock()
        service = AuditLogEntryServiceImpl(mock_repo)
        
        entry = service.log_account_state_change(
            username="admin",
            account_id=1,
            new_state="unlocked",
        )
        
        assert entry.account_id == 1
        assert entry.outcome == "account_unlocked"
        assert mock_repo.create.called

    def test_get_recent_logs(self) -> None:
        mock_repo = MagicMock()
        mock_repo.get_all.return_value = [MagicMock(), MagicMock()]
        service = AuditLogEntryServiceImpl(mock_repo)
        
        logs = service.get_recent_logs(skip=0, limit=10)
        
        assert len(logs) == 2
        mock_repo.get_all.assert_called_with(skip=0, limit=10)
