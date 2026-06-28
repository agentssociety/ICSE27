from __future__ import annotations

import pytest
from datetime import datetime, timedelta

from src.domain.alert.Alert import (
    Permission,
    State,
    User,
    Resource,
    BloodTypeResource,
    Operation,
    BloodTypeAlertOperation,
    Alert,
    AlertId,
    AlertCreatedEvent,
    AlertUpdatedEvent,
)

"""Unit tests for Alert domain

Related tasks: #30
"""


class TestPermission:
    def test_permission_values(self) -> None:
        assert Permission.READ.value == "read"
        assert Permission.WRITE.value == "write"
        assert Permission.EXECUTE.value == "execute"
        assert Permission.ADMIN.value == "admin"


class TestState:
    def test_state_values(self) -> None:
        assert State.PRE1.value == "pre1"
        assert State.POST1.value == "post1"
        assert State.EC_SAFETY_STALE.value == "ec_safety_stale"


class TestUser:
    def test_user_creation(self) -> None:
        user = User(userId="user1", mayPerform={Permission.READ, Permission.WRITE})
        assert user.userId == "user1"
        assert user.mayPerform == {Permission.READ, Permission.WRITE}

    def test_has_permission_valid(self) -> None:
        user = User(userId="user1", mayPerform={Permission.READ})
        assert user.hasPermission(Permission.READ) is True

    def test_has_permission_invalid(self) -> None:
        user = User(userId="user1", mayPerform={Permission.READ})
        assert user.hasPermission(Permission.WRITE) is False


class TestBloodTypeResource:
    def test_creation(self) -> None:
        resource = BloodTypeResource(bloodType="A+", units=50)
        assert resource.bloodType == "A+"
        assert resource.units == 50

    def test_is_accessible_with_manager(self) -> None:
        resource = BloodTypeResource(bloodType="A+", units=50)
        assert resource.isAccessible("manager1") is True

    def test_is_not_accessible_with_none(self) -> None:
        resource = BloodTypeResource(bloodType="A+", units=50)
        assert resource.isAccessible(None) is False


class TestBloodTypeAlertOperation:
    def test_create_valid(self) -> None:
        class MockInventoryPort:
            pass
        class MockNotificationPort:
            pass
        op = BloodTypeAlertOperation(
            inventoryPort=MockInventoryPort(),
            notificationPort=MockNotificationPort(),
        )
        blood_types = [
            BloodTypeResource(bloodType="A+", units=50),
            BloodTypeResource(bloodType="O-", units=30),
        ]
        op.create(manager="manager1", bloodTypes=blood_types)
        # Should not raise

    def test_create_with_none_manager(self) -> None:
        class MockInventoryPort:
            pass
        class MockNotificationPort:
            pass
        op = BloodTypeAlertOperation(
            inventoryPort=MockInventoryPort(),
            notificationPort=MockNotificationPort(),
        )
        with pytest.raises(ValueError, match="Manager cannot be None"):
            op.create(manager=None, bloodTypes=[BloodTypeResource(bloodType="A+", units=50)])

    def test_create_with_no_blood_types(self) -> None:
        class MockInventoryPort:
            pass
        class MockNotificationPort:
            pass
        op = BloodTypeAlertOperation(
            inventoryPort=MockInventoryPort(),
            notificationPort=MockNotificationPort(),
        )
        with pytest.raises(ValueError, match="At least one blood type must be provided"):
            op.create(manager="manager1", bloodTypes=[])

    def test_check_stock_low(self) -> None:
        class MockInventoryPort:
            pass
        class MockNotificationPort:
            pass
        op = BloodTypeAlertOperation(
            inventoryPort=MockInventoryPort(),
            notificationPort=MockNotificationPort(),
        )
        inventory = [
            BloodTypeResource(bloodType="A+", units=5),   # Low
            BloodTypeResource(bloodType="O-", units=15),  # OK
            BloodTypeResource(bloodType="B+", units=3),   # Low
        ]
        low_stock = op.checkStock(inventory)
        assert len(low_stock) == 2
        assert low_stock[0].bloodType == "A+"
        assert low_stock[1].bloodType == "B+"

    def test_check_stock_all_ok(self) -> None:
        class MockInventoryPort:
            pass
        class MockNotificationPort:
            pass
        op = BloodTypeAlertOperation(
            inventoryPort=MockInventoryPort(),
            notificationPort=MockNotificationPort(),
        )
        inventory = [
            BloodTypeResource(bloodType="A+", units=20),
            BloodTypeResource(bloodType="O-", units=30),
        ]
        low_stock = op.checkStock(inventory)
        assert len(low_stock) == 0

    def test_update_state_valid(self) -> None:
        class MockInventoryPort:
            pass
        class MockNotificationPort:
            pass
        op = BloodTypeAlertOperation(
            inventoryPort=MockInventoryPort(),
            notificationPort=MockNotificationPort(),
        )
        assert op.state == State.PRE1
        op.updateState(State.POST1)
        assert op.state == State.POST1

    def test_update_state_invalid(self) -> None:
        class MockInventoryPort:
            pass
        class MockNotificationPort:
            pass
        op = BloodTypeAlertOperation(
            inventoryPort=MockInventoryPort(),
            notificationPort=MockNotificationPort(),
            state=State.PRE1,
        )
        with pytest.raises(ValueError, match="Invalid state transition"):
            op.updateState(State.EC_SAFETY_STALE)

    def test_update_state_already_at_stale(self) -> None:
        class MockInventoryPort:
            pass
        class MockNotificationPort:
            pass
        op = BloodTypeAlertOperation(
            inventoryPort=MockInventoryPort(),
            notificationPort=MockNotificationPort(),
            state=State.POST1,
        )
        op.updateState(State.EC_SAFETY_STALE)
        assert op.state == State.EC_SAFETY_STALE


class TestAlert:
    def test_creation(self) -> None:
        alert = Alert(message="Low stock alert")
        assert alert.message == "Low stock alert"
        assert alert.state == State.PRE1
        assert alert.created_at is not None

    def test_set_message(self) -> None:
        alert = Alert(message="Initial")
        alert.setMessage("Updated")
        assert alert.message == "Updated"
        assert alert.updated_at is not None

    def test_is_not_stale(self) -> None:
        alert = Alert(message="Test")
        assert alert.isStale(max_age_hours=24) is False

    def test_is_stale(self) -> None:
        old_time = datetime.now() - timedelta(hours=48)
        alert = Alert(message="Test", created_at=old_time)
        assert alert.isStale(max_age_hours=24) is True


class TestAlertId:
    def test_creation(self) -> None:
        alert_id = AlertId(id="alert-001")
        assert alert_id.id == "alert-001"


class TestAlertEvents:
    def test_created_event(self) -> None:
        alert_id = AlertId(id="alert-001")
        event = AlertCreatedEvent(alert_id=alert_id)
        assert event.alert_id.id == "alert-001"
        assert event.timestamp is not None

    def test_updated_event(self) -> None:
        alert_id = AlertId(id="alert-001")
        event = AlertUpdatedEvent(alert_id=alert_id)
        assert event.alert_id.id == "alert-001"
        assert event.timestamp is not None
