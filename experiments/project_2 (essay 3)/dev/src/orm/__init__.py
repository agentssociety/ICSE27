# Register all ORM models for Alembic and SQLAlchemy metadata.
from src.orm.actor.actor_orm import ActorORM  # noqa: F401
from src.orm.blood_type.blood_type_orm import BloodTypeORM  # noqa: F401
from src.orm.blood_unit.blood_unit_orm import BloodUnitORM  # noqa: F401
from src.orm.patient_detail.patient_detail_orm import PatientDetailORM  # noqa: F401
from src.orm.reservation.reservation_orm import ReservationORM  # noqa: F401
from src.orm.resource.resource_orm import ResourceORM  # noqa: F401
from src.orm.transfusion_request.transfusion_request_orm import TransfusionRequestORM  # noqa: F401
