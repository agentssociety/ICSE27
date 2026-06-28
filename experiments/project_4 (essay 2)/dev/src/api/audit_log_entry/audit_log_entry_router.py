from __future__ import annotations



from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.audit_log_entry.audit_log_entry_dto import AuditLogEntryCreate, AuditLogEntryUpdate, AuditLogEntryResponse
from src.infra.audit_log_entry.audit_log_entry_repo_impl import SQLAlchemyAuditLogEntryRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyAuditLogEntryRepository:
    return SQLAlchemyAuditLogEntryRepository(db)


@router.get("", response_model=list[AuditLogEntryResponse])
def list_audit_log_entrys(skip: int = 0, limit: int = 100, repo: SQLAlchemyAuditLogEntryRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=AuditLogEntryResponse)
def get_audit_log_entry(item_id: int, repo: SQLAlchemyAuditLogEntryRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuditLogEntry not found")
    return item


@router.post("", response_model=AuditLogEntryResponse, status_code=status.HTTP_201_CREATED)
def create_audit_log_entry(data: AuditLogEntryCreate, repo: SQLAlchemyAuditLogEntryRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=AuditLogEntryResponse)
def update_audit_log_entry(item_id: int, data: AuditLogEntryUpdate, repo: SQLAlchemyAuditLogEntryRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuditLogEntry not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_audit_log_entry(item_id: int, repo: SQLAlchemyAuditLogEntryRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuditLogEntry not found")
