from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.interface.interface_dto import InterfaceCreate, InterfaceUpdate, InterfaceResponse
from src.infra.interface.interface_repo_impl import SQLAlchemyInterfaceRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyInterfaceRepository:
    return SQLAlchemyInterfaceRepository(db)


@router.get("", response_model=list[InterfaceResponse])
def list_interfaces(skip: int = 0, limit: int = 100, repo: SQLAlchemyInterfaceRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=InterfaceResponse)
def get_interface(item_id: int, repo: SQLAlchemyInterfaceRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interface not found")
    return item


@router.post("", response_model=InterfaceResponse, status_code=status.HTTP_201_CREATED)
def create_interface(data: InterfaceCreate, repo: SQLAlchemyInterfaceRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=InterfaceResponse)
def update_interface(item_id: int, data: InterfaceUpdate, repo: SQLAlchemyInterfaceRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interface not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interface(item_id: int, repo: SQLAlchemyInterfaceRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interface not found")
