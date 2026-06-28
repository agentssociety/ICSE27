# Register all ORM models for Alembic and SQLAlchemy metadata.
from src.orm.actor.actor_orm import ActorORM  # noqa: F401
from src.orm.blood_unit.blood_unit_orm import BloodUnitORM  # noqa: F401
from src.orm.reservation.reservation_orm import ReservationORM  # noqa: F401
from src.orm.resource.resource_orm import ResourceORM  # noqa: F401
