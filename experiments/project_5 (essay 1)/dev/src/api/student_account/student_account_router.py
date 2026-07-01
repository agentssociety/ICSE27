from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.student_account.student_account_dto import StudentAccountCreate, StudentAccountUpdate, StudentAccountResponse
from src.infra.student_account.student_account_repo_impl import SQLAlchemyStudentAccountRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyStudentAccountRepository:
    return SQLAlchemyStudentAccountRepository(db)


@router.get("", response_model=list[StudentAccountResponse])
def list_student_accounts(skip: int = 0, limit: int = 100, repo: SQLAlchemyStudentAccountRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=StudentAccountResponse)
def get_student_account(item_id: int, repo: SQLAlchemyStudentAccountRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="StudentAccount not found")
    return item


@router.post("", response_model=StudentAccountResponse, status_code=status.HTTP_201_CREATED)
def create_student_account(data: StudentAccountCreate, repo: SQLAlchemyStudentAccountRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=StudentAccountResponse)
def update_student_account(item_id: int, data: StudentAccountUpdate, repo: SQLAlchemyStudentAccountRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="StudentAccount not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_account(item_id: int, repo: SQLAlchemyStudentAccountRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="StudentAccount not found")
