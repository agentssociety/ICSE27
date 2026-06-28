from __future__ import annotations
import pytest
from datetime import datetime
from src.domain.flagged_transaction.FlaggedTransaction import (
    FlaggedTransaction,
    FlagStatus,
    DetectionEngine,
)
class TestFlaggedTransactionDomain:
    def test_create_flag(self) -> None:
        flagged = FlaggedTransaction.create(withdrawal_id='wd-001', reason='threshold')
        assert flagged.withdrawal_id == 'wd-001'
        assert flagged.reason == 'threshold'
        assert flagged.status == FlagStatus.UNREVIEWED
        assert flagged.reviewed_by is None
        assert flagged.id is not None
        assert len(flagged.id) > 0
    def test_mark_as_reviewed(self) -> None:
        flagged = FlaggedTransaction.create(withdrawal_id='wd-001', reason='velocity')
        flagged.mark_as_reviewed(reviewer_id='rev-001')
        assert flagged.status == FlagStatus.REVIEWED
        assert flagged.reviewed_by == 'rev-001'
    def test_mark_as_reviewed_changes_state(self) -> None:
        flagged = FlaggedTransaction.create(withdrawal_id='wd-001', reason='unusual_time')
        assert flagged.status == FlagStatus.UNREVIEWED
        flagged.mark_as_reviewed('admin-01')
        assert flagged.status == FlagStatus.REVIEWED
        assert flagged.reviewed_by == 'admin-01'
class TestDetectionEngine:
    def setup_method(self) -> None:
        self.engine = DetectionEngine()
    def _make_withdrawal(self, account_id, amount, hour=10):
        dt = datetime(2024, 6, 1, hour, 0, 0)
        return {'account_id': account_id, 'amount': amount, 'timestamp': dt}
    def test_velocity_trigger(self) -> None:
        wds = [self._make_withdrawal('acc-001', 100, 10) for _ in range(4)]
        reasons = self.engine.evaluate('wd-004', 'acc-001', 100, datetime(2024, 6, 1, 10, 30, 0), wds)
        assert 'velocity' in reasons
    def test_threshold_trigger(self) -> None:
        reasons = self.engine.evaluate('wd-big', 'acc-001', 15000, datetime(2024, 6, 1, 10, 0, 0), [])
        assert 'threshold' in reasons
    def test_unusual_time_trigger(self) -> None:
        reasons = self.engine.evaluate('wd-late', 'acc-001', 100, datetime(2024, 6, 1, 3, 30, 0), [])
        assert 'unusual_time' in reasons
    def test_no_flag_for_normal_withdrawal(self) -> None:
        reasons = self.engine.evaluate('wd-normal', 'acc-001', 100, datetime(2024, 6, 1, 10, 0, 0), [])
        assert len(reasons) == 0
    def test_threshold_not_reached(self) -> None:
        reasons = self.engine.evaluate('wd-small', 'acc-001', 10000, datetime(2024, 6, 1, 10, 0, 0), [])
        assert 'threshold' not in reasons
    def test_non_unusual_time(self) -> None:
        reasons = self.engine.evaluate('wd-normal', 'acc-001', 100, datetime(2024, 6, 1, 10, 0, 0), [])
        assert 'unusual_time' not in reasons
    def test_velocity_not_reached(self) -> None:
        wds = [self._make_withdrawal('acc-001', 100, 10) for _ in range(2)]
        reasons = self.engine.evaluate('wd-003', 'acc-001', 100, datetime(2024, 6, 1, 10, 30, 0), wds)
        assert 'velocity' not in reasons
