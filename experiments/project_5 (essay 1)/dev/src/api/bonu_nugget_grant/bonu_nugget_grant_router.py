from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.bonu_nugget_grant.bonu_nugget_grant_dto import BonuNuggetGrantCreate, BonuNuggetGrantUpdate, BonuNuggetGrantResponse
from src.infra.bonu_nugget_grant.bonu_nugget_grant_repo_impl import SQLAlchemyBonuNuggetGrantRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyBonuNuggetGrantRepository:
    return SQLAlchemyBonuNuggetGrantRepository(db)


@router.get("", response_model=list[BonuNuggetGrantResponse])
def list_bonu_nugget_grants(skip: int = 0, limit: int = 100, repo: SQLAlchemyBonuNuggetGrantRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=BonuNuggetGrantResponse)
def get_bonu_nugget_grant(item_id: int, repo: SQLAlchemyBonuNuggetGrantRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BonuNuggetGrant not found")
    return item


@router.post("", response_model=BonuNuggetGrantResponse, status_code=status.HTTP_201_CREATED)
def create_bonu_nugget_grant(data: BonuNuggetGrantCreate, db: Session = Depends(get_db)):
    from src.infra.nugget_wallet.nugget_wallet_repo_impl import SQLAlchemyNuggetWalletRepository
    from src.infra.audit_event.audit_event_repo_impl import SQLAlchemyAuditEventRepository
    from src.dto.audit_event.audit_event_dto import AuditEventCreate

    repo = SQLAlchemyBonuNuggetGrantRepository(db)
    grant = repo.create(data)

    wallet_repo = SQLAlchemyNuggetWalletRepository(db)
    wallet_repo.add_nuggets(data.student_id, data.amount)

    audit_repo = SQLAlchemyAuditEventRepository(db)
    audit_repo.create(AuditEventCreate(
        event_type="bonus_nugget_grant",
        instructor_id=data.instructor_id,
        student_id=data.student_id,
        amount=data.amount,
        justification=data.justification,
    ))
    return grant


@router.put("/{item_id}", response_model=BonuNuggetGrantResponse)
def update_bonu_nugget_grant(item_id: int, data: BonuNuggetGrantUpdate, repo: SQLAlchemyBonuNuggetGrantRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BonuNuggetGrant not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bonu_nugget_grant(item_id: int, repo: SQLAlchemyBonuNuggetGrantRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BonuNuggetGrant not found")
