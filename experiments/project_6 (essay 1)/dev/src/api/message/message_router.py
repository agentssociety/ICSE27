from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.message.message_dto import MessageCreate, MessageUpdate, MessageResponse
from src.infra.message.message_repo_impl import SQLAlchemyMessageRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyMessageRepository:
    return SQLAlchemyMessageRepository(db)


@router.get("", response_model=list[MessageResponse])
def list_messages(skip: int = 0, limit: int = 100, repo: SQLAlchemyMessageRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=MessageResponse)
def get_message(item_id: int, repo: SQLAlchemyMessageRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return item


@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_message(data: MessageCreate, repo: SQLAlchemyMessageRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=MessageResponse)
def update_message(item_id: int, data: MessageUpdate, repo: SQLAlchemyMessageRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(item_id: int, repo: SQLAlchemyMessageRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
