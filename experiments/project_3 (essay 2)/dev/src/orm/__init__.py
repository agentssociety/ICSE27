# Register all ORM models for Alembic and SQLAlchemy metadata.
from src.orm.alternative_runway.alternative_runway_orm import AlternativeRunwayORM  # noqa: F401
from src.orm.channel.channel_orm import ChannelORM  # noqa: F401
from src.orm.flight.flight_orm import FlightORM  # noqa: F401
from src.orm.interface.interface_orm import InterfaceORM  # noqa: F401
from src.orm.operation.operation_orm import OperationORM  # noqa: F401
from src.orm.resource.resource_orm import ResourceORM  # noqa: F401
from src.orm.runway.runway_orm import RunwayORM  # noqa: F401
from src.orm.slot.slot_orm import SlotORM  # noqa: F401
from src.orm.time_slot.time_slot_orm import TimeSlotORM  # noqa: F401
