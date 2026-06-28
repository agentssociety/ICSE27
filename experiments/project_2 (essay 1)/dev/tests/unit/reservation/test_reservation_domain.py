from __future__ import annotations

import pytest
from datetime import datetime

from src.domain.reservation.Reservation import (
    Permission,
    IfaceKind,
    State,
    Actor,
    Resource,
    Interface,
    Scheduling_API,
    Blood_Inventory_Database,
    REQ_BB_01,
    CancellationRecord,
    OverlapRecord,
    OutageRecord,
    Reservation,
    ReservationId,
    ReservationCreatedEvent,
    ReservationUpdatedEvent,
)

"""Unit tests for Reservation domain

Related tasks: #28
"""


class TestPermission:
    def test_permission_values(self) -> None:
        assert Permission.READ.value == "read"
        assert Permission.WRITE.value == "write"
        assert Permission.EXECUTE.value == "execute"
        assert Permission.ADMIN.value == "admin"


class TestIfaceKind:
    def test_iface_kind_values(self) -> None:
        assert IfaceKind.API.value == "api"
        assert IfaceKind.DATABASE.value == "database"


class TestState:
    def test_state_creation(self) -> None:
        state = State(name="TestState")
        assert state.name == "TestState"

    def test_available_state(self) -> None:
        state = State.available()
        assert state.name == "Available"

    def test_reserved_state(self) -> None:
        state = State.reserved()
        assert state.name == "Reserved"

    def test_canceled_state(self) -> None:
        state = State.canceled()
        assert state.name == "Canceled"

    def test_state_equality(self) -> None:
        state1 = State.available()
        state2 = State.available()
        state3 = State.reserved()
        assert state1 == state2
        assert state1 != state3

    def test_check_state_change_available_to_reserved(self) -> None:
        available = State.available()
        reserved = State.reserved()
        # From Available, can go to Reserved
        assert available.checkStateChange(available, reserved) is True

    def test_check_state_change_reserved_to_canceled(self) -> None:
        reserved = State.reserved()
        canceled = State.canceled()
        # From Reserved, can go to Canceled
        assert reserved.checkStateChange(reserved, canceled) is True

    def test_check_state_change_invalid(self) -> None:
        completed = State.completed()
        expired = State.expired()
        # From Completed: cannot go to any other state
        assert completed.checkStateChange(completed, expired) is False

    def test_transition_state_valid(self) -> None:
        available = State.available()
        reserved = State.reserved()
        result = available.transitionState(available, reserved)
        assert result == reserved

    def test_transition_state_invalid(self) -> None:
        completed = State.completed()
        reserved = State.reserved()
        with pytest.raises(ValueError, match="Invalid state transition"):
            completed.transitionState(completed, reserved)


class TestActor:
    def test_creation(self) -> None:
        actor = Actor(actorId="act1", mayPerform=frozenset({Permission.READ, Permission.WRITE}))
        assert Permission.READ in actor.mayPerform
        assert Permission.WRITE in actor.mayPerform
        assert Permission.ADMIN not in actor.mayPerform

    def test_check_permission_valid(self) -> None:
        actor = Actor(actorId="act1", mayPerform=frozenset({Permission.READ}))
        assert actor.checkPermission(actor, Permission.READ) is True

    def test_check_permission_invalid(self) -> None:
        actor = Actor(actorId="act1", mayPerform=frozenset({Permission.READ}))
        assert actor.checkPermission(actor, Permission.WRITE) is False


class TestResource:
    def test_creation(self) -> None:
        actor = Actor(actorId="act1", mayPerform=frozenset({Permission.READ}))
        resource = Resource(owner=actor, accessible={actor})
        assert resource.owner == actor
        assert actor in resource.accessible

    def test_check_access_owner(self) -> None:
        actor = Actor(actorId="act1", mayPerform=frozenset({Permission.READ}))
        resource = Resource(owner=actor)
        assert resource.checkAccess(actor, resource) is True

    def test_check_access_in_accessible_set(self) -> None:
        actor1 = Actor(actorId="act1", mayPerform=frozenset({Permission.READ}))
        actor2 = Actor(actorId="act2", mayPerform=frozenset({Permission.READ}))
        resource = Resource(owner=actor1, accessible={actor2})
        assert resource.checkAccess(actor2, resource) is True

    def test_check_access_no_access(self) -> None:
        actor1 = Actor(actorId="act1", mayPerform=frozenset({Permission.READ}))
        actor2 = Actor(actorId="act2", mayPerform=frozenset({Permission.READ}))
        resource = Resource(owner=actor1)
        assert resource.checkAccess(actor2, resource) is False


class TestInterface:
    def test_creation(self) -> None:
        iface = Interface(kind=IfaceKind.API, encrypted=True, authenticated=True)
        assert iface.kind == IfaceKind.API
        assert iface.encrypted is True
        assert iface.authenticated is True

    def test_check_authentication(self) -> None:
        iface = Interface(kind=IfaceKind.API, authenticated=True)
        assert iface.checkAuthentication(iface) is True

    def test_check_authentication_fails(self) -> None:
        iface = Interface(kind=IfaceKind.API, authenticated=False)
        assert iface.checkAuthentication(iface) is False


class TestBloodInventoryDatabase:
    def test_query_reservation(self) -> None:
        db = Blood_Inventory_Database()
        state = db.queryReservation("unit-001")
        assert state == State.available()

    def test_release_reservation(self) -> None:
        db = Blood_Inventory_Database()
        result = db.releaseReservation("unit-001")
        assert result is True

    def test_update_reservation_status(self) -> None:
        db = Blood_Inventory_Database()
        result = db.updateReservationStatus("unit-001", State.reserved())
        assert result is True


class TestREQ_BB_01:
    def test_create_operation_valid(self) -> None:
        actor = Actor(actorId="act1", mayPerform=frozenset({Permission.WRITE}))
        iface = Interface(kind=IfaceKind.API, authenticated=True)
        resource = Resource(owner=actor, accessible={actor})
        op = REQ_BB_01(
            initiator=actor,
            target=[resource],
            channel={iface},
            grant=Permission.WRITE,
            pre=State.available(),
            post=State.reserved(),
        )
        op.createOperation()  # Should not raise

    def test_create_operation_no_channel(self) -> None:
        actor = Actor(actorId="act1", mayPerform=frozenset({Permission.WRITE}))
        resource = Resource(owner=actor, accessible={actor})
        op = REQ_BB_01(
            initiator=actor,
            target=[resource],
            channel=set(),
            grant=Permission.WRITE,
            pre=State.available(),
            post=State.reserved(),
        )
        with pytest.raises(ValueError, match="Operation requires at least one channel"):
            op.createOperation()

    def test_create_operation_no_target(self) -> None:
        actor = Actor(actorId="act1", mayPerform=frozenset({Permission.WRITE}))
        iface = Interface(kind=IfaceKind.API, authenticated=True)
        op = REQ_BB_01(
            initiator=actor,
            target=[],
            channel={iface},
            grant=Permission.WRITE,
            pre=State.available(),
            post=State.reserved(),
        )
        with pytest.raises(ValueError, match="Operation requires at least one target resource"):
            op.createOperation()

    def test_create_operation_no_permission(self) -> None:
        actor = Actor(actorId="act1", mayPerform=frozenset({Permission.READ}))
        iface = Interface(kind=IfaceKind.API, authenticated=True)
        resource = Resource(owner=actor, accessible={actor})
        op = REQ_BB_01(
            initiator=actor,
            target=[resource],
            channel={iface},
            grant=Permission.WRITE,
            pre=State.available(),
            post=State.reserved(),
        )
        with pytest.raises(PermissionError, match="Initiator does not have write permission"):
            op.createOperation()

    def test_create_operation_no_state_change(self) -> None:
        actor = Actor(actorId="act1", mayPerform=frozenset({Permission.WRITE}))
        iface = Interface(kind=IfaceKind.API, authenticated=True)
        resource = Resource(owner=actor, accessible={actor})
        op = REQ_BB_01(
            initiator=actor,
            target=[resource],
            channel={iface},
            grant=Permission.WRITE,
            pre=State.available(),
            post=State.available(),
        )
        with pytest.raises(ValueError, match="Operation must involve at least one state change"):
            op.createOperation()

    def test_create_operation_no_resource_access(self) -> None:
        actor1 = Actor(actorId="act1", mayPerform=frozenset({Permission.WRITE}))
        actor2 = Actor(actorId="act2", mayPerform=frozenset({Permission.WRITE}))
        iface = Interface(kind=IfaceKind.API, authenticated=True)
        resource = Resource(owner=actor2)  # actor2 is owner, not actor1
        op = REQ_BB_01(
            initiator=actor1,
            target=[resource],
            channel={iface},
            grant=Permission.WRITE,
            pre=State.available(),
            post=State.reserved(),
        )
        with pytest.raises(PermissionError, match="Initiator does not have access to target resource"):
            op.createOperation()


class TestCancellationRecord:
    def test_create_cancellation_record_valid(self) -> None:
        actor = Actor(actorId="act1", mayPerform=frozenset({Permission.WRITE}))
        iface = Interface(kind=IfaceKind.API, authenticated=True)
        resource = Resource(owner=actor, accessible={actor})
        op = REQ_BB_01(
            initiator=actor,
            target=[resource],
            channel={iface},
            grant=Permission.WRITE,
            pre=State.reserved(),
            post=State.canceled(),
        )
        record = CancellationRecord.createCancellationRecord(
            op=op, resource=resource, time_state=State.canceled()
        )
        assert record.op == op
        assert record.resource == resource
        assert record.time == State.canceled()

    def test_create_cancellation_record_invalid_permission(self) -> None:
        actor = Actor(actorId="act1", mayPerform=frozenset({Permission.READ}))
        iface = Interface(kind=IfaceKind.API, authenticated=True)
        resource = Resource(owner=actor, accessible={actor})
        op = REQ_BB_01(
            initiator=actor,
            target=[resource],
            channel={iface},
            grant=Permission.READ,
            pre=State.reserved(),
            post=State.canceled(),
        )
        with pytest.raises(PermissionError, match="Cancellation requires WRITE or ADMIN permission"):
            CancellationRecord.createCancellationRecord(
                op=op, resource=resource, time_state=State.canceled()
            )


class TestOverlapRecord:
    def test_record_overlap_valid(self) -> None:
        actor = Actor(actorId="act1", mayPerform=frozenset({Permission.WRITE}))
        iface = Interface(kind=IfaceKind.API, authenticated=True)
        resource = Resource(owner=actor, accessible={actor})
        op1 = REQ_BB_01(
            initiator=actor,
            target=[resource],
            channel={iface},
            grant=Permission.WRITE,
            pre=State.available(),
            post=State.reserved(),
        )
        op2 = REQ_BB_01(
            initiator=actor,
            target=[resource],
            channel={iface},
            grant=Permission.WRITE,
            pre=State.reserved(),
            post=State.canceled(),
        )
        overlap = OverlapRecord.recordOverlap(resource=resource, first_op=op1, second_op=op2)
        assert overlap.resource == resource
        assert overlap.first == op1
        assert overlap.second == op2

    def test_record_overlap_invalid(self) -> None:
        actor = Actor(actorId="act1", mayPerform=frozenset({Permission.WRITE}))
        iface = Interface(kind=IfaceKind.API, authenticated=True)
        resource1 = Resource(owner=actor, accessible={actor})
        actor2 = Actor(actorId="act2", mayPerform=frozenset({Permission.WRITE}))
        resource2 = Resource(owner=actor2, accessible={actor2})
        op1 = REQ_BB_01(
            initiator=actor,
            target=[resource1],
            channel={iface},
            grant=Permission.WRITE,
            pre=State.available(),
            post=State.reserved(),
        )
        op2 = REQ_BB_01(
            initiator=actor,
            target=[resource2],
            channel={iface},
            grant=Permission.WRITE,
            pre=State.reserved(),
            post=State.canceled(),
        )
        with pytest.raises(ValueError, match="Resource must be a target of both operations"):
            OverlapRecord.recordOverlap(resource=resource1, first_op=op1, second_op=op2)


class TestOutageRecord:
    def test_create_outage_record_valid(self) -> None:
        record = OutageRecord.createOutageRecord(op=None, reason="System Outage")
        assert record.op is None
        assert record.reason == "System Outage"

    def test_create_outage_record_empty_reason(self) -> None:
        with pytest.raises(ValueError, match="Reason for outage must be provided"):
            OutageRecord.createOutageRecord(op=None, reason="")


class TestReservation:
    def test_creation(self) -> None:
        reservation = Reservation()
        assert reservation.state == State.available()
        assert reservation.created_at is not None

    def test_set_state_valid(self) -> None:
        reservation = Reservation()
        reservation.setState(State.reserved())
        assert reservation.state == State.reserved()

    def test_set_state_invalid(self) -> None:
        reservation = Reservation()
        with pytest.raises(ValueError, match="Invalid state transition"):
            reservation.setState(State.expired())


class TestReservationId:
    def test_creation(self) -> None:
        res_id = ReservationId(id="res-001")
        assert res_id.id == "res-001"


class TestReservationEvents:
    def test_created_event(self) -> None:
        res_id = ReservationId(id="res-001")
        event = ReservationCreatedEvent(reservation_id=res_id)
        assert event.reservation_id.id == "res-001"
        assert event.timestamp is not None

    def test_updated_event(self) -> None:
        res_id = ReservationId(id="res-001")
        event = ReservationUpdatedEvent(reservation_id=res_id)
        assert event.reservation_id.id == "res-001"
        assert event.timestamp is not None
