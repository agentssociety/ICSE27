from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.nugget_wallet.nugget_wallet_dto import NuggetWalletCreate, NuggetWalletUpdate, NuggetWalletResponse
from src.orm.nugget_wallet.nugget_wallet_orm import NuggetWalletORM


class SQLAlchemyNuggetWalletRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[NuggetWalletResponse]:
        row = self._session.get(NuggetWalletORM, item_id)
        return NuggetWalletResponse.model_validate(row) if row else None

    def get_by_student_id(self, student_id: int) -> Optional[NuggetWalletResponse]:
        row = self._session.query(NuggetWalletORM).filter(NuggetWalletORM.student_id == student_id).first()
        return NuggetWalletResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[NuggetWalletResponse]:
        rows = self._session.query(NuggetWalletORM).offset(skip).limit(limit).all()
        return [NuggetWalletResponse.model_validate(r) for r in rows]

    def create(self, data: NuggetWalletCreate) -> NuggetWalletResponse:
        row = NuggetWalletORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return NuggetWalletResponse.model_validate(row)

    def update(self, item_id: int, data: NuggetWalletUpdate) -> Optional[NuggetWalletResponse]:
        row = self._session.get(NuggetWalletORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return NuggetWalletResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(NuggetWalletORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True

    def add_nuggets(self, student_id: int, amount: float) -> Optional[NuggetWalletResponse]:
        row = self._session.query(NuggetWalletORM).filter(NuggetWalletORM.student_id == student_id).first()
        if row is None:
            return None
        row.balance = (row.balance or 0.0) + amount
        self._session.commit()
        self._session.refresh(row)
        return NuggetWalletResponse.model_validate(row)

    def deduct_nuggets(self, student_id: int, amount: float) -> Optional[NuggetWalletResponse]:
        row = self._session.query(NuggetWalletORM).filter(NuggetWalletORM.student_id == student_id).first()
        if row is None or (row.balance or 0.0) < amount:
            return None
        row.balance = (row.balance or 0.0) - amount
        self._session.commit()
        self._session.refresh(row)
        return NuggetWalletResponse.model_validate(row)
