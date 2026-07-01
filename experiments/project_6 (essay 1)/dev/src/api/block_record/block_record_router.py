from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.block_record.block_record_dto import BlockRecordCreate, BlockRecordUpdate, BlockRecordResponse
from src.infra.block_record.block_record_repo_impl import SQLAlchemyBlockRecordRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyBlockRecordRepository:
    return SQLAlchemyBlockRecordRepository(db)


@router.get("", response_model=list[BlockRecordResponse])
def list_block_records(skip: int = 0, limit: int = 100, repo: SQLAlchemyBlockRecordRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=BlockRecordResponse)
def get_block_record(item_id: int, repo: SQLAlchemyBlockRecordRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BlockRecord not found")
    return item


@router.post("", response_model=BlockRecordResponse, status_code=status.HTTP_201_CREATED)
def create_block_record(data: BlockRecordCreate, repo: SQLAlchemyBlockRecordRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=BlockRecordResponse)
def update_block_record(item_id: int, data: BlockRecordUpdate, repo: SQLAlchemyBlockRecordRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BlockRecord not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_block_record(item_id: int, repo: SQLAlchemyBlockRecordRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BlockRecord not found")
