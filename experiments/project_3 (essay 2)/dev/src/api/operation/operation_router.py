from __future__ import annotations


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.operation.operation_dto import OperationCreate, OperationUpdate, OperationResponse
from src.infra.operation.operation_repo_impl import SQLAlchemyOperationRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyOperationRepository:
    return SQLAlchemyOperationRepository(db)


@router.get("", response_model=list[OperationResponse])
def list_operations(skip: int = 0, limit: int = 100, repo: SQLAlchemyOperationRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=OperationResponse)
def get_operation(item_id: int, repo: SQLAlchemyOperationRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operation not found")
    return item


@router.post("", response_model=OperationResponse, status_code=status.HTTP_201_CREATED)
def create_operation(data: OperationCreate, repo: SQLAlchemyOperationRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=OperationResponse)
def update_operation(item_id: int, data: OperationUpdate, repo: SQLAlchemyOperationRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operation not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_operation(item_id: int, repo: SQLAlchemyOperationRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operation not found")
