from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.registration_data.registration_data_dto import RegistrationDataCreate, RegistrationDataUpdate, RegistrationDataResponse
from src.infra.registration_data.registration_data_repo_impl import SQLAlchemyRegistrationDataRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyRegistrationDataRepository:
    return SQLAlchemyRegistrationDataRepository(db)


@router.get("", response_model=list[RegistrationDataResponse])
def list_registration_datas(skip: int = 0, limit: int = 100, repo: SQLAlchemyRegistrationDataRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=RegistrationDataResponse)
def get_registration_data(item_id: int, repo: SQLAlchemyRegistrationDataRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RegistrationData not found")
    return item


@router.post("", response_model=RegistrationDataResponse, status_code=status.HTTP_201_CREATED)
def create_registration_data(data: RegistrationDataCreate, repo: SQLAlchemyRegistrationDataRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=RegistrationDataResponse)
def update_registration_data(item_id: int, data: RegistrationDataUpdate, repo: SQLAlchemyRegistrationDataRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RegistrationData not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_registration_data(item_id: int, repo: SQLAlchemyRegistrationDataRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RegistrationData not found")
