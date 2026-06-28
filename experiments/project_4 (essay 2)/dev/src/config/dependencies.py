from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.infra.audit_log_entry.audit_log_entry_repo_impl import SQLAlchemyAuditLogEntryRepository


def get_audit_log_entry_repository(db: Session = Depends(get_db)) -> SQLAlchemyAuditLogEntryRepository:
    return SQLAlchemyAuditLogEntryRepository(db)
