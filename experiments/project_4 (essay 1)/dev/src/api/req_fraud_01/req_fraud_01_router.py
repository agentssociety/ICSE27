from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.req_fraud_01.req_fraud_01_dto import REQ_FRAUD_01Create, REQ_FRAUD_01Update, REQ_FRAUD_01Response
from src.infra.req_fraud_01.req_fraud_01_repo_impl import SQLAlchemyREQ_FRAUD_01Repository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyREQ_FRAUD_01Repository:
    return SQLAlchemyREQ_FRAUD_01Repository(db)


@router.get("", response_model=list[REQ_FRAUD_01Response])
def list_req_fraud_01s(skip: int = 0, limit: int = 100, repo: SQLAlchemyREQ_FRAUD_01Repository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=REQ_FRAUD_01Response)
def get_req_fraud_01(item_id: int, repo: SQLAlchemyREQ_FRAUD_01Repository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="REQ_FRAUD_01 not found")
    return item


@router.post("", response_model=REQ_FRAUD_01Response, status_code=status.HTTP_201_CREATED)
def create_req_fraud_01(data: REQ_FRAUD_01Create, repo: SQLAlchemyREQ_FRAUD_01Repository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=REQ_FRAUD_01Response)
def update_req_fraud_01(item_id: int, data: REQ_FRAUD_01Update, repo: SQLAlchemyREQ_FRAUD_01Repository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="REQ_FRAUD_01 not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_req_fraud_01(item_id: int, repo: SQLAlchemyREQ_FRAUD_01Repository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="REQ_FRAUD_01 not found")
