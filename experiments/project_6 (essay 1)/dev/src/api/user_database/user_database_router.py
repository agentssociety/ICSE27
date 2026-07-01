from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.user_database.user_database_dto import User_DatabaseCreate, User_DatabaseUpdate, User_DatabaseResponse
from src.infra.user_database.user_database_repo_impl import SQLAlchemyUser_DatabaseRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyUser_DatabaseRepository:
    return SQLAlchemyUser_DatabaseRepository(db)


@router.get("", response_model=list[User_DatabaseResponse])
def list_user_databases(skip: int = 0, limit: int = 100, repo: SQLAlchemyUser_DatabaseRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=User_DatabaseResponse)
def get_user_database(item_id: int, repo: SQLAlchemyUser_DatabaseRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User_Database not found")
    return item


@router.post("", response_model=User_DatabaseResponse, status_code=status.HTTP_201_CREATED)
def create_user_database(data: User_DatabaseCreate, repo: SQLAlchemyUser_DatabaseRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=User_DatabaseResponse)
def update_user_database(item_id: int, data: User_DatabaseUpdate, repo: SQLAlchemyUser_DatabaseRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User_Database not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_database(item_id: int, repo: SQLAlchemyUser_DatabaseRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User_Database not found")
