from __future__ import annotations


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.channel.channel_dto import ChannelCreate, ChannelUpdate, ChannelResponse
from src.infra.channel.channel_repo_impl import SQLAlchemyChannelRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyChannelRepository:
    return SQLAlchemyChannelRepository(db)


@router.get("", response_model=list[ChannelResponse])
def list_channels(skip: int = 0, limit: int = 100, repo: SQLAlchemyChannelRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ChannelResponse)
def get_channel(item_id: int, repo: SQLAlchemyChannelRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
    return item


@router.post("", response_model=ChannelResponse, status_code=status.HTTP_201_CREATED)
def create_channel(data: ChannelCreate, repo: SQLAlchemyChannelRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=ChannelResponse)
def update_channel(item_id: int, data: ChannelUpdate, repo: SQLAlchemyChannelRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_channel(item_id: int, repo: SQLAlchemyChannelRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
