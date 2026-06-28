from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.card.card_dto import CardCreateRequest, CardUpdateRequest, CardResponse
from src.infra.card.card_repo_impl import SQLAlchemyCardRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyCardRepository:
    return SQLAlchemyCardRepository(db)


@router.get("", response_model=list[CardResponse])
def list_cards(skip: int = 0, limit: int = 100, repo: SQLAlchemyCardRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=CardResponse)
def get_card(item_id: str, repo: SQLAlchemyCardRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    return item


@router.post("", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
def create_card(data: CardCreateRequest, repo: SQLAlchemyCardRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=CardResponse)
def update_card(item_id: str, data: CardUpdateRequest, repo: SQLAlchemyCardRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(item_id: str, repo: SQLAlchemyCardRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")


class CardRouter:
    def __init__(self) -> None:
        pass
