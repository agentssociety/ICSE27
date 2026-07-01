from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.resource.resource_dto import ResourceCreate, ResourceUpdate, ResourceResponse
from src.infra.resource.resource_repo_impl import SQLAlchemyResourceRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyResourceRepository:
    return SQLAlchemyResourceRepository(db)


@router.get("", response_model=list[ResourceResponse])
def list_resources(skip: int = 0, limit: int = 100, repo: SQLAlchemyResourceRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ResourceResponse)
def get_resource(item_id: int, repo: SQLAlchemyResourceRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return item


@router.post("", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
def create_resource(data: ResourceCreate, repo: SQLAlchemyResourceRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=ResourceResponse)
def update_resource(item_id: int, data: ResourceUpdate, repo: SQLAlchemyResourceRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(item_id: int, repo: SQLAlchemyResourceRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
