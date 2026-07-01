from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.audit_log.audit_log_dto import AuditLogCreate, AuditLogUpdate, AuditLogResponse
from src.infra.audit_log.audit_log_repo_impl import SQLAlchemyAuditLogRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyAuditLogRepository:
    return SQLAlchemyAuditLogRepository(db)


@router.get("", response_model=list[AuditLogResponse])
def list_audit_logs(skip: int = 0, limit: int = 100, repo: SQLAlchemyAuditLogRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=AuditLogResponse)
def get_audit_log(item_id: int, repo: SQLAlchemyAuditLogRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuditLog not found")
    return item


@router.post("", response_model=AuditLogResponse, status_code=status.HTTP_201_CREATED)
def create_audit_log(data: AuditLogCreate, repo: SQLAlchemyAuditLogRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=AuditLogResponse)
def update_audit_log(item_id: int, data: AuditLogUpdate, repo: SQLAlchemyAuditLogRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuditLog not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_audit_log(item_id: int, repo: SQLAlchemyAuditLogRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuditLog not found")
