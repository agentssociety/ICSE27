from __future__ import annotations

from typing import Optional, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.infra.separation_rule.separation_rule_repo_impl import SQLAlchemySeparationRuleRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemySeparationRuleRepository:
    return SQLAlchemySeparationRuleRepository(db)


@router.get("", response_model=list[Any])
def list_separation_rules(skip: int = 0, limit: int = 100, repo: SQLAlchemySeparationRuleRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=Any)
def get_separation_rule(item_id: int, repo: SQLAlchemySeparationRuleRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SeparationRule not found")
    return item


@router.post("", response_model=Any, status_code=status.HTTP_201_CREATED)
def create_separation_rule(data: Any, repo: SQLAlchemySeparationRuleRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=Any)
def update_separation_rule(item_id: int, data: Any, repo: SQLAlchemySeparationRuleRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SeparationRule not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_separation_rule(item_id: int, repo: SQLAlchemySeparationRuleRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SeparationRule not found")