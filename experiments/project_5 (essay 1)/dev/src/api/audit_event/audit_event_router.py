from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.audit_event.audit_event_dto import AuditEventCreate, AuditEventResponse
from src.infra.audit_event.audit_event_repo_impl import SQLAlchemyAuditEventRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyAuditEventRepository:
    return SQLAlchemyAuditEventRepository(db)


@router.get("", response_model=list[AuditEventResponse])
def list_audit_events(skip: int = 0, limit: int = 100, repo: SQLAlchemyAuditEventRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=AuditEventResponse)
def get_audit_event(item_id: int, repo: SQLAlchemyAuditEventRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuditEvent not found")
    return item
