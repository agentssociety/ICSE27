from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.audit_entry.audit_entry_dto import AuditEntryCreate, AuditEntryUpdate, AuditEntryResponse
from src.infra.audit_entry.audit_entry_repo_impl import SQLAlchemyAuditEntryRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyAuditEntryRepository:
    return SQLAlchemyAuditEntryRepository(db)


@router.get("", response_model=list[AuditEntryResponse])
def list_audit_entrys(skip: int = 0, limit: int = 100, repo: SQLAlchemyAuditEntryRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=AuditEntryResponse)
def get_audit_entry(item_id: int, repo: SQLAlchemyAuditEntryRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuditEntry not found")
    return item


@router.post("", response_model=AuditEntryResponse, status_code=status.HTTP_201_CREATED)
def create_audit_entry(data: AuditEntryCreate, repo: SQLAlchemyAuditEntryRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=AuditEntryResponse)
def update_audit_entry(item_id: int, data: AuditEntryUpdate, repo: SQLAlchemyAuditEntryRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuditEntry not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_audit_entry(item_id: int, repo: SQLAlchemyAuditEntryRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuditEntry not found")
