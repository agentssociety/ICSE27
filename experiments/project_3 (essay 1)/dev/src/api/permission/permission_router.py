from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.permission.permission_dto import PermissionCreate, PermissionUpdate, PermissionResponse
from src.infra.permission.permission_repo_impl import SQLAlchemyPermissionRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyPermissionRepository:
    return SQLAlchemyPermissionRepository(db)


@router.get("", response_model=list[PermissionResponse])
def list_permissions(skip: int = 0, limit: int = 100, repo: SQLAlchemyPermissionRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=PermissionResponse)
def get_permission(item_id: int, repo: SQLAlchemyPermissionRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    return item


@router.post("", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
def create_permission(data: PermissionCreate, repo: SQLAlchemyPermissionRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=PermissionResponse)
def update_permission(item_id: int, data: PermissionUpdate, repo: SQLAlchemyPermissionRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(item_id: int, repo: SQLAlchemyPermissionRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
