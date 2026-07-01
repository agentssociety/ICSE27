from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.redemption.redemption_dto import RedemptionCreate, RedemptionUpdate, RedemptionResponse
from src.infra.redemption.redemption_repo_impl import SQLAlchemyRedemptionRepository
from src.infra.nugget_wallet.nugget_wallet_repo_impl import SQLAlchemyNuggetWalletRepository
from src.infra.reward_item.reward_item_repo_impl import SQLAlchemyRewardItemRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyRedemptionRepository:
    return SQLAlchemyRedemptionRepository(db)


@router.get("", response_model=list[RedemptionResponse])
def list_redemptions(skip: int = 0, limit: int = 100, student_id: Optional[int] = None,
                     repo: SQLAlchemyRedemptionRepository = Depends(_repo)):
    if student_id is not None:
        return repo.get_by_student_id(student_id)
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=RedemptionResponse)
def get_redemption(item_id: int, repo: SQLAlchemyRedemptionRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Redemption not found")
    return item


@router.post("", response_model=RedemptionResponse, status_code=status.HTTP_201_CREATED)
def create_redemption(data: RedemptionCreate, db: Session = Depends(get_db)):
    repo = SQLAlchemyRedemptionRepository(db)
    wallet_repo = SQLAlchemyNuggetWalletRepository(db)
    item_repo = SQLAlchemyRewardItemRepository(db)

    reward_item = item_repo.get_by_id(data.reward_item_id)
    if reward_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RewardItem not found")

    wallet = wallet_repo.deduct_nuggets(data.student_id, reward_item.cost)
    if wallet is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient nugget balance")

    redemption_data = RedemptionCreate(
        student_id=data.student_id,
        reward_item_id=data.reward_item_id,
        nuggets_spent=reward_item.cost,
    )
    return repo.create(redemption_data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_redemption(item_id: int, repo: SQLAlchemyRedemptionRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Redemption not found")
