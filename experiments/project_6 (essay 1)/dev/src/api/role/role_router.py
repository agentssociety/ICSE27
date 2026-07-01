from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.role.role_dto import RoleCreate, RoleUpdate, RoleResponse
from src.infra.role.role_repo_impl import SQLAlchemyRoleRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyRoleRepository:
    return SQLAlchemyRoleRepository(db)


@router.get("", response_model=list[RoleResponse])
def list_roles(skip: int = 0, limit: int = 100, repo: SQLAlchemyRoleRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=RoleResponse)
def get_role(item_id: int, repo: SQLAlchemyRoleRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return item


@router.post("", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(data: RoleCreate, repo: SQLAlchemyRoleRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=RoleResponse)
def update_role(item_id: int, data: RoleUpdate, repo: SQLAlchemyRoleRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(item_id: int, repo: SQLAlchemyRoleRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
