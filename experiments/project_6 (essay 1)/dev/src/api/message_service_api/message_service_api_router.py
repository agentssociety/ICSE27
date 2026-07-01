from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.message_service_api.message_service_api_dto import Message_Service_APICreate, Message_Service_APIUpdate, Message_Service_APIResponse
from src.infra.message_service_api.message_service_api_repo_impl import SQLAlchemyMessage_Service_APIRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyMessage_Service_APIRepository:
    return SQLAlchemyMessage_Service_APIRepository(db)


@router.get("", response_model=list[Message_Service_APIResponse])
def list_message_service_apis(skip: int = 0, limit: int = 100, repo: SQLAlchemyMessage_Service_APIRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=Message_Service_APIResponse)
def get_message_service_api(item_id: int, repo: SQLAlchemyMessage_Service_APIRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message_Service_API not found")
    return item


@router.post("", response_model=Message_Service_APIResponse, status_code=status.HTTP_201_CREATED)
def create_message_service_api(data: Message_Service_APICreate, repo: SQLAlchemyMessage_Service_APIRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=Message_Service_APIResponse)
def update_message_service_api(item_id: int, data: Message_Service_APIUpdate, repo: SQLAlchemyMessage_Service_APIRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message_Service_API not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message_service_api(item_id: int, repo: SQLAlchemyMessage_Service_APIRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message_Service_API not found")
