from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.bookmark.bookmark_dto import BookmarkCreate, BookmarkUpdate, BookmarkResponse
from src.infra.bookmark.bookmark_repo_impl import SQLAlchemyBookmarkRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyBookmarkRepository:
    return SQLAlchemyBookmarkRepository(db)


@router.get("", response_model=list[BookmarkResponse])
def list_bookmarks(skip: int = 0, limit: int = 100, repo: SQLAlchemyBookmarkRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=BookmarkResponse)
def get_bookmark(item_id: int, repo: SQLAlchemyBookmarkRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark not found")
    return item


@router.post("", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED)
def create_bookmark(data: BookmarkCreate, repo: SQLAlchemyBookmarkRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=BookmarkResponse)
def update_bookmark(item_id: int, data: BookmarkUpdate, repo: SQLAlchemyBookmarkRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bookmark(item_id: int, repo: SQLAlchemyBookmarkRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark not found")
