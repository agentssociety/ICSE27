from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.biography.biography_dto import BiographyCreate, BiographyUpdate, BiographyResponse
from src.infra.biography.biography_repo_impl import SQLAlchemyBiographyRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyBiographyRepository:
    return SQLAlchemyBiographyRepository(db)


@router.get("", response_model=list[BiographyResponse])
def list_biographys(skip: int = 0, limit: int = 100, repo: SQLAlchemyBiographyRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=BiographyResponse)
def get_biography(item_id: int, repo: SQLAlchemyBiographyRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Biography not found")
    return item


@router.post("", response_model=BiographyResponse, status_code=status.HTTP_201_CREATED)
def create_biography(data: BiographyCreate, repo: SQLAlchemyBiographyRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=BiographyResponse)
def update_biography(item_id: int, data: BiographyUpdate, repo: SQLAlchemyBiographyRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Biography not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_biography(item_id: int, repo: SQLAlchemyBiographyRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Biography not found")
