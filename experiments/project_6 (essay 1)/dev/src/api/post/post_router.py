from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.post.post_dto import PostCreateDTO, PostUpdateDTO, PostResponseDTO
from src.infra.post.post_repo_impl import SQLAlchemyPostRepository

"""
Api layer for the Post domain class

Package: api.post
Layer: api
Related tasks: #159, #160, #161, #162, #167, #169, #170, #171, #172, #178
Requirement coverage:
- User can create a text post and optionally upload images
- User can like and unlike a post
- Add, edit, and delete comments on posts
- Display News Feed Sorted by Time
- Group Post Feed Filter
"""

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyPostRepository:
    return SQLAlchemyPostRepository(db)


@router.get("", response_model=list[PostResponseDTO])
def list_posts(skip: int = 0, limit: int = 100, repo: SQLAlchemyPostRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=PostResponseDTO)
def get_post(item_id: int, repo: SQLAlchemyPostRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return item


@router.post("", response_model=PostResponseDTO, status_code=status.HTTP_201_CREATED)
def create_post(data: PostCreateDTO, repo: SQLAlchemyPostRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=PostResponseDTO)
def update_post(item_id: int, data: PostUpdateDTO, repo: SQLAlchemyPostRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(item_id: int, repo: SQLAlchemyPostRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
