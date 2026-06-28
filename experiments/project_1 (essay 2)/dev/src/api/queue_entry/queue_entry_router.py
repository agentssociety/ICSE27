from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.queue_entry.queue_entry_dto import QueueEntryCreate, QueueEntryUpdate, QueueEntryResponse
from src.infra.queue_entry.queue_entry_repo_impl import SQLAlchemyQueueEntryRepository

router = APIRouter()

def _repo(db: Session = Depends(get_db)) -> SQLAlchemyQueueEntryRepository:
    return SQLAlchemyQueueEntryRepository(db)

@router.get("", response_model=list[QueueEntryResponse])
def list_queue_entrys(skip: int = 0, limit: int = 100, repo: SQLAlchemyQueueEntryRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)

@router.get("/{item_id}", response_model=QueueEntryResponse)
def get_queue_entry(item_id: int, repo: SQLAlchemyQueueEntryRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="QueueEntry not found")
    return item

@router.post("", response_model=QueueEntryResponse, status_code=status.HTTP_201_CREATED)
def create_queue_entry(data: QueueEntryCreate, repo: SQLAlchemyQueueEntryRepository = Depends(_repo)):
    return repo.create(data)

@router.put("/{item_id}", response_model=QueueEntryResponse)
def update_queue_entry(item_id: int, data: QueueEntryUpdate, repo: SQLAlchemyQueueEntryRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="QueueEntry not found")
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_queue_entry(item_id: int, repo: SQLAlchemyQueueEntryRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="QueueEntry not found")