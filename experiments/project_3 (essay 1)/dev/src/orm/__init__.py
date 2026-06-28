# Register all ORM models for Alembic and SQLAlchemy metadata.
from src.orm.aircraft.aircraft_orm import AircraftORM  # noqa: F401
from src.orm.emergency_flight.emergency_flight_orm import EmergencyFlightORM  # noqa: F401
from src.orm.flight.flight_orm import FlightORM  # noqa: F401
from src.orm.interface.interface_orm import InterfaceORM  # noqa: F401
from src.orm.operation.operation_orm import OperationORM  # noqa: F401
from src.orm.operation_slot.operation_slot_orm import OperationSlotORM  # noqa: F401
from src.orm.permission.permission_orm import PermissionORM  # noqa: F401
from src.orm.resource.resource_orm import ResourceORM  # noqa: F401
from src.orm.runway.runway_orm import RunwayORM  # noqa: F401
from src.orm.separation_rule.separation_rule_orm import SeparationRuleORM  # noqa: F401
from src.orm.slot.slot_orm import SlotORM  # noqa: F401
from src.orm.state.state_orm import StateORM  # noqa: F401
from src.orm.traffic_data.traffic_data_orm import TrafficDataORM  # noqa: F401
