from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.block.block_dto import BlockCreate, BlockUpdate, BlockResponse
from src.infra.block.block_repo_impl import SQLAlchemyBlockRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyBlockRepository:
    return SQLAlchemyBlockRepository(db)


@router.get("", response_model=list[BlockResponse])
def list_blocks(skip: int = 0, limit: int = 100, repo: SQLAlchemyBlockRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=BlockResponse)
def get_block(item_id: int, repo: SQLAlchemyBlockRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Block not found")
    return item


@router.post("", response_model=BlockResponse, status_code=status.HTTP_201_CREATED)
def create_block(data: BlockCreate, repo: SQLAlchemyBlockRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=BlockResponse)
def update_block(item_id: int, data: BlockUpdate, repo: SQLAlchemyBlockRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Block not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_block(item_id: int, repo: SQLAlchemyBlockRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Block not found")
