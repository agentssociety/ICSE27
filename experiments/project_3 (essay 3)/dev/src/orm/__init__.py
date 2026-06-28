# Register all ORM models for Alembic and SQLAlchemy metadata.
from src.orm.actor.actor_orm import ActorORM  # noqa: F401
from src.orm.flight.flight_orm import FlightORM  # noqa: F401
from src.orm.interface.interface_orm import InterfaceORM  # noqa: F401
from src.orm.resource.resource_orm import ResourceORM  # noqa: F401
from src.orm.runway.runway_orm import RunwayORM  # noqa: F401
