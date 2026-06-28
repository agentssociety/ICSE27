from __future__ import annotations

from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import uuid4


class FlagStatus(Enum):
    UNREVIEWED = "unreviewed"
    REVIEWED = "reviewed"


@dataclass
class FlaggedTransaction:
    id: str
    withdrawal_id: str
    reason: str
    flagged_at: datetime
    reviewed_by: Optional[str] = None
    status: FlagStatus = FlagStatus.UNREVIEWED

    @classmethod
    def create(cls, withdrawal_id: str, reason: str) -> FlaggedTransaction:
        return cls(
            id=str(uuid4()),
            withdrawal_id=withdrawal_id,
            reason=reason,
            flagged_at=datetime.utcnow(),
            reviewed_by=None,
            status=FlagStatus.UNREVIEWED,
        )

    def mark_as_reviewed(self, reviewer_id: str) -> None:
        self.reviewed_by = reviewer_id
        self.status = FlagStatus.REVIEWED


class DetectionEngine:
    def __init__(
        self,
        threshold_amount: float = 10000.0,
        velocity_count: int = 3,
        velocity_window_minutes: int = 60,
    ):
        self.threshold_amount = threshold_amount
        self.velocity_count = velocity_count
        self.velocity_window_minutes = velocity_window_minutes

    def evaluate(
        self,
        withdrawal_id: str,
        account_id: str,
        amount: float,
        timestamp: datetime,
        all_withdrawals: list[dict],
    ) -> list[str]:
        reasons: list[str] = []
        if self._check_velocity(account_id, timestamp, all_withdrawals):
            reasons.append("velocity")
        if self._check_threshold(amount):
            reasons.append("threshold")
        if self._check_unusual_time(timestamp):
            reasons.append("unusual_time")
        return reasons

    def _check_velocity(self, account_id: str, timestamp: datetime, all_withdrawals: list[dict]) -> bool:
        from datetime import timedelta
        window_start = timestamp - timedelta(minutes=self.velocity_window_minutes)
        count = 0
        for w in all_withdrawals:
            w_ts = w.get("timestamp")
            if w_ts is None:
                continue
            if isinstance(w_ts, str):
                from datetime import datetime as dt2
                w_ts = dt2.fromisoformat(w_ts)
            if w.get("account_id") == account_id and w_ts >= window_start and w_ts <= timestamp:
                count += 1
        return count > self.velocity_count

    def _check_threshold(self, amount: float) -> bool:
        return amount > self.threshold_amount

    def _check_unusual_time(self, timestamp: datetime) -> bool:
        hour = timestamp.hour
        return 2 <= hour < 5

