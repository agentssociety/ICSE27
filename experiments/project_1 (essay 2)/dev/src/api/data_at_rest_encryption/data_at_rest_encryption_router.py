from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.data_at_rest_encryption.data_at_rest_encryption_dto import DataAtRestEncryptionCreate, DataAtRestEncryptionUpdate, DataAtRestEncryptionResponse
from src.infra.data_at_rest_encryption.data_at_rest_encryption_repo_impl import SQLAlchemyDataAtRestEncryptionRepository

router = APIRouter()

def _repo(db: Session = Depends(get_db)) -> SQLAlchemyDataAtRestEncryptionRepository:
    return SQLAlchemyDataAtRestEncryptionRepository(db)

@router.get("", response_model=list[DataAtRestEncryptionResponse])
def list_data_at_rest_encryptions(skip: int = 0, limit: int = 100, repo: SQLAlchemyDataAtRestEncryptionRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)

@router.get("/{item_id}", response_model=DataAtRestEncryptionResponse)
def get_data_at_rest_encryption(item_id: int, repo: SQLAlchemyDataAtRestEncryptionRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DataAtRestEncryption not found")
    return item

@router.post("", response_model=DataAtRestEncryptionResponse, status_code=status.HTTP_201_CREATED)
def create_data_at_rest_encryption(data: DataAtRestEncryptionCreate, repo: SQLAlchemyDataAtRestEncryptionRepository = Depends(_repo)):
    return repo.create(data)

@router.put("/{item_id}", response_model=DataAtRestEncryptionResponse)
def update_data_at_rest_encryption(item_id: int, data: DataAtRestEncryptionUpdate, repo: SQLAlchemyDataAtRestEncryptionRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DataAtRestEncryption not found")
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data_at_rest_encryption(item_id: int, repo: SQLAlchemyDataAtRestEncryptionRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DataAtRestEncryption not found")