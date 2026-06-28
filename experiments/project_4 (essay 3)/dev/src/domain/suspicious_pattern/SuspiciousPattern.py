from __future__ import annotations

from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from decimal import Decimal
from uuid import uuid4

"""
Domain layer for the SuspiciousPattern domain class

Package: domain.suspicious_pattern
Layer: domain
Related tasks: None
Requirement coverage:
- Detection and Flagging of Suspicious Withdrawal Patterns
"""


class PatternType(Enum):
    """Types of suspicious withdrawal patterns that can be detected."""
    VELOCITY = "velocity"
    THRESHOLD = "threshold"
    UNUSUAL_TIME = "unusual_time"
    RAPID_SUCCESSIVE = "rapid_successive"
    ROUND_AMOUNT = "round_amount"
    STRUCTURED = "structured"


class ReviewStatus(Enum):
    """Status of a suspicious pattern review."""
    UNREVIEWED = "unreviewed"
    UNDER_REVIEW = "under_review"
    CONFIRMED = "confirmed"
    DISMISSED = "dismissed"


@dataclass
class SuspiciousPattern:
    """Core domain model for suspicious withdrawal pattern detection.

    Defines a pattern to detect suspicious withdrawal behaviour, including
    the pattern type, threshold that triggers it, and whether it is active.
    """
    patternType: PatternType
    threshold: float
    active: bool
    withdrawalTransaction: Optional[Any] = None  # WithdrawalTransaction (forward reference)
    account: Optional[Any] = None  # Account (forward reference)
    id: str = ""
    detected_at: Optional[str] = None
    review_status: ReviewStatus = ReviewStatus.UNREVIEWED

    def __post_init__(self) -> None:
        if not self.id:
            self.id = str(uuid4())

    @classmethod
    def create(
        cls,
        patternType: PatternType,
        threshold: float,
        active: bool = True,
    ) -> SuspiciousPattern:
        """Factory method to create a new suspicious pattern."""
        if threshold <= 0:
            raise ValueError("Threshold must be positive")
        return cls(
            patternType=patternType,
            threshold=threshold,
            active=active,
            id=str(uuid4()),
        )

    def evaluatePattern(
        self,
        transaction: Any,  # WithdrawalTransaction
        initiator: Any,    # Actor / Security_Team / Finance_Team / Operations_Team
        target: Any,       # Resource / Transaction_Database
    ) -> bool:
        """Evaluate whether a transaction matches this suspicious pattern.

        Returns True if the transaction is flagged as suspicious based on
        the pattern type and threshold.
        """
        if not self.active:
            return False
        if transaction is None:
            return False

        # Extract amount and timestamp from the transaction
        # Support both object attributes and dict access
        if hasattr(transaction, "amount"):
            amount = float(transaction.amount)
            timestamp = getattr(transaction, "timestamp", datetime.utcnow())
        elif isinstance(transaction, dict):
            amount = float(transaction.get("amount", 0))
            timestamp = transaction.get("timestamp", datetime.utcnow())
        else:
            return False

        if isinstance(timestamp, str):
            from datetime import datetime as dt_parse
            try:
                timestamp = dt_parse.fromisoformat(timestamp)
            except ValueError:
                timestamp = datetime.utcnow()

        if self.patternType == PatternType.VELOCITY:
            return self._evaluate_velocity_pattern(transaction, amount, timestamp)
        elif self.patternType == PatternType.THRESHOLD:
            return self._evaluate_threshold_pattern(amount)
        elif self.patternType == PatternType.UNUSUAL_TIME:
            return self._evaluate_unusual_time_pattern(timestamp)
        elif self.patternType == PatternType.RAPID_SUCCESSIVE:
            return self._evaluate_rapid_successive_pattern(transaction, timestamp)
        elif self.patternType == PatternType.ROUND_AMOUNT:
            return self._evaluate_round_amount_pattern(amount)
        elif self.patternType == PatternType.STRUCTURED:
            return self._evaluate_structured_pattern(transaction, amount)
        return False

    def _evaluate_velocity_pattern(self, transaction: Any, amount: float, timestamp: datetime) -> bool:
        """Check if there are too many withdrawals in a short time window."""
        velocity_window_minutes = 60  # Default 1-hour window
        velocity_count = int(self.threshold) if self.threshold > 0 else 3

        # Check if transaction has context about recent withdrawals
        if hasattr(transaction, "all_withdrawals"):
            all_withdrawals = transaction.all_withdrawals
        elif isinstance(transaction, dict) and "all_withdrawals" in transaction:
            all_withdrawals = transaction["all_withdrawals"]
        else:
            # Without context, just check if this single transaction exceeds threshold
            return amount > self.threshold

        # Count withdrawals in the velocity window
        window_start = timestamp - timedelta(minutes=velocity_window_minutes)
        count = 0
        for w in all_withdrawals:
            w_ts = w.get("timestamp") if isinstance(w, dict) else getattr(w, "timestamp", None)
            w_amount = float(w.get("amount", 0)) if isinstance(w, dict) else float(getattr(w, "amount", 0))
            if w_ts is None:
                continue
            if isinstance(w_ts, str):
                from datetime import datetime as dt_parse
                try:
                    w_ts = dt_parse.fromisoformat(w_ts)
                except ValueError:
                    continue
            if window_start <= w_ts <= timestamp:
                count += 1
                if count > velocity_count:
                    return True
        return False

    def _evaluate_threshold_pattern(self, amount: float) -> bool:
        """Check if the withdrawal amount exceeds the configured threshold."""
        return amount > self.threshold

    def _evaluate_unusual_time_pattern(self, timestamp: datetime) -> bool:
        """Check if the withdrawal occurs during unusual hours (2-5 AM)."""
        hour = timestamp.hour
        return 2 <= hour < 5

    def _evaluate_rapid_successive_pattern(self, transaction: Any, timestamp: datetime) -> bool:
        """Check if multiple withdrawals happen in rapid succession."""
        rapid_window_minutes = 15
        rapid_count = 2  # At least 2 withdrawals in 15 minutes

        if hasattr(transaction, "all_withdrawals"):
            all_withdrawals = transaction.all_withdrawals
        elif isinstance(transaction, dict) and "all_withdrawals" in transaction:
            all_withdrawals = transaction["all_withdrawals"]
        else:
            return False

        window_start = timestamp - timedelta(minutes=rapid_window_minutes)
        count = 0
        for w in all_withdrawals:
            w_ts = w.get("timestamp") if isinstance(w, dict) else getattr(w, "timestamp", None)
            if w_ts is None:
                continue
            if isinstance(w_ts, str):
                from datetime import datetime as dt_parse
                try:
                    w_ts = dt_parse.fromisoformat(w_ts)
                except ValueError:
                    continue
            if window_start <= w_ts <= timestamp:
                count += 1
                if count >= rapid_count:
                    return True
        return False

    def _evaluate_round_amount_pattern(self, amount: float) -> bool:
        """Check if the withdrawal amount is a round number (e.g., 5000, 10000)."""
        return amount >= self.threshold and (amount % 1000 == 0)

    def _evaluate_structured_pattern(self, transaction: Any, amount: float) -> bool:
        """Check for structured withdrawals just below reporting thresholds."""
        # Structured deposits/withdrawals are often just below $10,000
        reporting_threshold = 10000.0
        threshold_margin = 500.0
        return (reporting_threshold - threshold_margin) <= amount < reporting_threshold

    def activate(self) -> None:
        """Activate this suspicious pattern for detection."""
        self.active = True

    def deactivate(self) -> None:
        """Deactivate this suspicious pattern."""
        self.active = False

    def is_active(self) -> bool:
        """Check if this pattern is active."""
        return self.active

    def mark_reviewed(self, status: ReviewStatus) -> None:
        """Mark the pattern as reviewed with the given status."""
        self.review_status = status
        self.detected_at = datetime.utcnow().isoformat()

    def matches_pattern(self, transaction: Any) -> bool:
        """Convenience method to check if a transaction matches this pattern."""
        return self.evaluatePattern(transaction, None, None)


# Type alias to avoid forward reference issues
Any = object


@dataclass
class SuspiciousPatternId:
    """Value object for SuspiciousPattern ID."""
    pass


@dataclass
class SuspiciousPatternCreatedEvent:
    """Event emitted when a suspicious pattern is created."""
    pass


@dataclass
class SuspiciousPatternUpdatedEvent:
    """Event emitted when a suspicious pattern is updated."""
    pass
