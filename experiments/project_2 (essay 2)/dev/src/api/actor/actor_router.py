from __future__ import annotations



from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.actor.actor_dto import ActorCreate, ActorUpdate, ActorResponse
from src.infra.actor.actor_repo_impl import SQLAlchemyActorRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyActorRepository:
    return SQLAlchemyActorRepository(db)


@router.get("", response_model=list[ActorResponse])
def list_actors(skip: int = 0, limit: int = 100, repo: SQLAlchemyActorRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ActorResponse)
def get_actor(item_id: int, repo: SQLAlchemyActorRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Actor not found")
    return item


@router.post("", response_model=ActorResponse, status_code=status.HTTP_201_CREATED)
def create_actor(data: ActorCreate, repo: SQLAlchemyActorRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=ActorResponse)
def update_actor(item_id: int, data: ActorUpdate, repo: SQLAlchemyActorRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Actor not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_actor(item_id: int, repo: SQLAlchemyActorRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Actor not found")
