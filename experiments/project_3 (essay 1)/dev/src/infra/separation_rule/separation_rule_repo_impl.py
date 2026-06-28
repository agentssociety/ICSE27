from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.separation_rule.separation_rule_dto import SeparationRuleCreate, SeparationRuleUpdate, SeparationRuleResponse
from src.orm.separation_rule.separation_rule_orm import SeparationRuleORM


class SQLAlchemySeparationRuleRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: int) -> Optional[SeparationRuleResponse]:
        row = self._session.get(SeparationRuleORM, item_id)
        return SeparationRuleResponse.model_validate(row) if row else None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SeparationRuleResponse]:
        rows = self._session.query(SeparationRuleORM).offset(skip).limit(limit).all()
        return [SeparationRuleResponse.model_validate(r) for r in rows]

    def create(self, data: SeparationRuleCreate) -> SeparationRuleResponse:
        row = SeparationRuleORM(**data.model_dump(exclude_unset=True))
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return SeparationRuleResponse.model_validate(row)

    def update(self, item_id: int, data: SeparationRuleUpdate) -> Optional[SeparationRuleResponse]:
        row = self._session.get(SeparationRuleORM, item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        self._session.commit()
        self._session.refresh(row)
        return SeparationRuleResponse.model_validate(row)

    def delete(self, item_id: int) -> bool:
        row = self._session.get(SeparationRuleORM, item_id)
        if row is None:
            return False
        self._session.delete(row)
        self._session.commit()
        return True
