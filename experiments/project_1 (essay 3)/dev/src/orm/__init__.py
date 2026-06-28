# Register all ORM models for Alembic and SQLAlchemy metadata.
from src.orm.actor.actor_orm import ActorORM  # noqa: F401
from src.orm.interface.interface_orm import InterfaceORM  # noqa: F401
from src.orm.patient.patient_orm import PatientORM  # noqa: F401
from src.orm.resource.resource_orm import ResourceORM  # noqa: F401
from src.orm.symptom.symptom_orm import SymptomORM  # noqa: F401
from src.orm.symptom_record.symptom_record_orm import SymptomRecordORM  # noqa: F401
from src.orm.user_authentication_system.user_authentication_system_orm import UserAuthenticationSystemORM  # noqa: F401
