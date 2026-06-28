from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.audit_log_resource.audit_log_resource_dto import AuditLogResourceCreate, AuditLogResourceUpdate, AuditLogResourceResponse
from src.infra.audit_log_resource.audit_log_resource_repo_impl import SQLAlchemyAuditLogResourceRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyAuditLogResourceRepository:
    return SQLAlchemyAuditLogResourceRepository(db)


@router.get("", response_model=list[AuditLogResourceResponse])
def list_audit_log_resources(skip: int = 0, limit: int = 100, repo: SQLAlchemyAuditLogResourceRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=AuditLogResourceResponse)
def get_audit_log_resource(item_id: int, repo: SQLAlchemyAuditLogResourceRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuditLogResource not found")
    return item


@router.post("", response_model=AuditLogResourceResponse, status_code=status.HTTP_201_CREATED)
def create_audit_log_resource(data: AuditLogResourceCreate, repo: SQLAlchemyAuditLogResourceRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=AuditLogResourceResponse)
def update_audit_log_resource(item_id: int, data: AuditLogResourceUpdate, repo: SQLAlchemyAuditLogResourceRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuditLogResource not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_audit_log_resource(item_id: int, repo: SQLAlchemyAuditLogResourceRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AuditLogResource not found")
