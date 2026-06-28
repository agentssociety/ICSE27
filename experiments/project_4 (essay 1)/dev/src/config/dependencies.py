from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import get_db


def get_account_repository(db: Session = Depends(get_db)):
    from src.infra.account.account_repo_impl import SQLAlchemyAccountRepository
    return SQLAlchemyAccountRepository(db)


def get_actor_repository(db: Session = Depends(get_db)):
    from src.infra.actor.actor_repo_impl import SQLAlchemyActorRepository
    return SQLAlchemyActorRepository(db)


def get_card_repository(db: Session = Depends(get_db)):
    from src.infra.card.card_repo_impl import SQLAlchemyCardRepository
    return SQLAlchemyCardRepository(db)


def get_money_repository(db: Session = Depends(get_db)):
    from src.infra.money.money_repo_impl import SQLAlchemyMoneyRepository
    return SQLAlchemyMoneyRepository(db)


def get_pin_repository(db: Session = Depends(get_db)):
    from src.infra.pin.pin_repo_impl import SQLAlchemyPINRepository
    return SQLAlchemyPINRepository(db)


def get_transaction_repository(db: Session = Depends(get_db)):
    from src.infra.transaction.transaction_repo_impl import SQLAlchemyTransactionRepository
    return SQLAlchemyTransactionRepository(db)


def get_user_repository(db: Session = Depends(get_db)):
    from src.infra.user.user_repo_impl import SQLAlchemyUserRepository
    return SQLAlchemyUserRepository(db)


def get_withdrawal_record_repository(db: Session = Depends(get_db)):
    from src.infra.withdrawal_record.withdrawal_record_repo_impl import (
        SQLAlchemyWithdrawalRecordRepository,
    )
    return SQLAlchemyWithdrawalRecordRepository(db)