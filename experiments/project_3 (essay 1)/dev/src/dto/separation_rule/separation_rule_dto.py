from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

try:
    from src.domain.aircraft import WakeTurbulenceCategory
except ImportError:
    class WakeTurbulenceCategory:
        pass

try:
    from src.common.time import Duration
except ImportError:
    class Duration:
        pass


class SeparationRuleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class SeparationRuleCreate(SeparationRuleBase):
    wakeTurbulenceSeparation: dict[
        tuple[WakeTurbulenceCategory, WakeTurbulenceCategory], Duration
    ]


class SeparationRuleUpdate(SeparationRuleBase):
    wakeTurbulenceSeparation: Optional[
        dict[tuple[WakeTurbulenceCategory, WakeTurbulenceCategory], Duration]
    ] = None


class SeparationRuleResponse(SeparationRuleBase):
    id: int
    wakeTurbulenceSeparation: dict[
        tuple[WakeTurbulenceCategory, WakeTurbulenceCategory], Duration
    ]