# Project 8 — Scaffold Reference

Auto-generated from the persisted package design, requirement artifacts, and UML diagrams.
Intended as a navigation aid for follow-up agents and developers.

---

## Statistics

| Item | Count |
|------|-------|
| Packages | 27 |
| Requirements linked | 6 |
| Tasks | 6 |
| Domain classes | 3 |

---

## Notes

- Generated files are implementation skeletons intended to be filled in by follow-up agents or developers.
- Existing files are preserved unless `overwrite_existing=True` is used.

---

## File Index

All generated files organised by package.

### `domain.patient` · layer: `domain`

Path: `src/domain/patient`
> Domain layer for the Patient domain class

| File | Classes |
|------|---------|
| `Patient.py` | `Patient`, `Symptom`, `SymptomRecord`, `UserAuthenticationSystem`, `Permission`, `SymptomState`, `PatientId`, `PatientCreatedEvent`, `PatientUpdatedEvent` |

### `dto.patient` · layer: `dto`

Path: `src/dto/patient`
> Dto layer for the Patient domain class

| File | Classes |
|------|---------|
| `patient_dto.py` | `SymptomRequestDTO`, `SymptomResponseDTO`, `ErrorResponseDTO` |

### `repository.patient` · layer: `repository`

Path: `src/repository/patient`
> Repository layer for the Patient domain class

| File | Classes |
|------|---------|
| `patient_repository.py` | `SymptomRegistrationAPI`, `PatientDatabase`, `PatientUI` |

### `orm.patient` · layer: `orm`

Path: `src/orm/patient`
> Orm layer for the Patient domain class

| File | Classes |
|------|---------|
| `patient_orm.py` | `PatientORM` |

### `infra.patient` · layer: `infra`

Path: `src/infra/patient`
> Infra layer for the Patient domain class

| File | Classes |
|------|---------|
| `patient_repo_impl.py` | `SQLAlchemyPatientRepository` |

### `service.patient` · layer: `service`

Path: `src/service/patient`
> Service layer for the Patient domain class

| File | Classes |
|------|---------|
| `patient_service.py` | `PatientService`, `PatientServiceImpl` |

### `api.patient` · layer: `api`

Path: `src/api/patient`
> Api layer for the Patient domain class

| File | Classes |
|------|---------|
| `patient_router.py` | `SymptomController` |

### `tests.unit.patient` · layer: `tests`

Path: `tests/unit/patient`
> Unit tests for Patient across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_patient_domain.py` | — |
| `test_patient_service.py` | — |
| `test_patient_api.py` | — |

### `domain.urgency_level` · layer: `domain`

Path: `src/domain/urgency_level`
> Domain layer for the UrgencyLevel domain class

| File | Classes |
|------|---------|
| `UrgencyLevel.py` | `UrgencyLevel`, `Permission`, `Actor`, `Resource`, `State`, `Interface`, `IfaceKind`, `UrgencyLevelId`, `UrgencyLevelCreatedEvent`, `UrgencyLevelUpdatedEvent` |

### `dto.urgency_level` · layer: `dto`

Path: `src/dto/urgency_level`
> Dto layer for the UrgencyLevel domain class

| File | Classes |
|------|---------|
| `urgency_level_dto.py` | `UrgencyLevelCreateRequest`, `UrgencyLevelUpdateRequest`, `UrgencyLevelResponse` |

### `repository.urgency_level` · layer: `repository`

Path: `src/repository/urgency_level`
> Repository layer for the UrgencyLevel domain class

| File | Classes |
|------|---------|
| `urgency_level_repository.py` | `Item_Management_API` |

### `orm.urgency_level` · layer: `orm`

Path: `src/orm/urgency_level`
> Orm layer for the UrgencyLevel domain class

| File | Classes |
|------|---------|
| `urgency_level_orm.py` | `UrgencyLevelORM` |

### `infra.urgency_level` · layer: `infra`

Path: `src/infra/urgency_level`
> Infra layer for the UrgencyLevel domain class

| File | Classes |
|------|---------|
| `urgency_level_repo_impl.py` | `SQLAlchemyUrgencyLevelRepository` |

### `service.urgency_level` · layer: `service`

Path: `src/service/urgency_level`
> Service layer for the UrgencyLevel domain class

| File | Classes |
|------|---------|
| `urgency_level_service.py` | `REQ_ITEM_URGENCY_01` |

### `api.urgency_level` · layer: `api`

Path: `src/api/urgency_level`
> Api layer for the UrgencyLevel domain class

| File | Classes |
|------|---------|
| `urgency_level_router.py` | `UrgencyLevelRouter` |

### `tests.unit.urgency_level` · layer: `tests`

Path: `tests/unit/urgency_level`
> Unit tests for UrgencyLevel across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_urgency_level_domain.py` | — |
| `test_urgency_level_service.py` | — |
| `test_urgency_level_api.py` | — |

### `domain.queue` · layer: `domain`

Path: `src/domain/queue`
> Domain layer for the Queue domain class

| File | Classes |
|------|---------|
| `Queue.py` | `Queue`, `QueueItem`, `QueueId`, `QueueCreatedEvent`, `QueueUpdatedEvent` |

### `dto.queue` · layer: `dto`

Path: `src/dto/queue`
> Dto layer for the Queue domain class

| File | Classes |
|------|---------|
| `queue_dto.py` | `QueueCreateRequest`, `QueueUpdateRequest`, `QueueResponse` |

### `repository.queue` · layer: `repository`

Path: `src/repository/queue`
> Repository layer for the Queue domain class

| File | Classes |
|------|---------|
| `queue_repository.py` | `QueueRepository` |

### `orm.queue` · layer: `orm`

Path: `src/orm/queue`
> Orm layer for the Queue domain class

| File | Classes |
|------|---------|
| `queue_orm.py` | `QueueORM` |

### `infra.queue` · layer: `infra`

Path: `src/infra/queue`
> Infra layer for the Queue domain class

| File | Classes |
|------|---------|
| `queue_repo_impl.py` | `SQLAlchemyQueueRepository` |

### `service.queue` · layer: `service`

Path: `src/service/queue`
> Service layer for the Queue domain class

| File | Classes |
|------|---------|
| `queue_service.py` | `QueueService`, `QueueServiceImpl` |

### `api.queue` · layer: `api`

Path: `src/api/queue`
> Api layer for the Queue domain class

| File | Classes |
|------|---------|
| `queue_router.py` | `QueueRouter` |

### `tests.unit.queue` · layer: `tests`

Path: `tests/unit/queue`
> Unit tests for Queue across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_queue_domain.py` | — |
| `test_queue_service.py` | — |
| `test_queue_api.py` | — |

### `config.settings` · layer: `config`

Path: `src/config`
> Application settings, environment variables, dependency injection

| File | Classes |
|------|---------|
| `settings.py` | `Settings` |
| `dependencies.py` | `Container` |
| `database.py` | — |
| `logging.py` | — |

### `docs.api_and_deployment` · layer: `docs`

Path: `docs`
> OpenAPI documentation, admin guide, multi-city config, deployment runbook

*(no files specified)*

### `tests.integration` · layer: `tests`

Path: `tests/integration`
> End-to-end and cross-service integration tests

| File | Classes |
|------|---------|
| `test_patient_flow.py` | — |
| `test_urgency_level_flow.py` | — |
| `test_queue_flow.py` | — |
| `test_api_contracts.py` | — |
| `conftest.py` | — |

---

## Task Index

For each task: full description, files whose classes appear in the task's UML diagram,
and paths to the linked requirement specification and UML diagrams.

### Task #53 — Register patient with symptoms

**As a** patient
**I need** to register my symptoms
**So that** the system can handle my case

### Details and Assumptions
* The user is a patient with symptoms to report
* The system needs to process and store symptom information

### Acceptance Criteria

```gherkin
Given I am a patient
When I register my symptoms
Then the system records my symptom information
```

**UML class diagram:** `experiments/project_8/class_diagram_53.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/patient/patient_router.py` | `SymptomController` |
| `src/domain/patient/Patient.py` | `Patient`, `Permission`, `Symptom`, `SymptomRecord`, `SymptomState`, `UserAuthenticationSystem` |
| `src/domain/urgency_level/UrgencyLevel.py` | `Permission` |
| `src/dto/patient/patient_dto.py` | `ErrorResponseDTO`, `SymptomRequestDTO`, `SymptomResponseDTO` |
| `src/repository/patient/patient_repository.py` | `PatientDatabase`, `PatientUI`, `SymptomRegistrationAPI` |

---

### Task #54 — Assign urgency level (1-5)

**As a** user
**I need** to assign an urgency level (1-5)
**So that** I can prioritize items based on urgency

### Details and Assumptions
* The urgency level is a numeric scale from 1 to 5 (1 being lowest urgency, 5 being highest).
* Items can have their urgency level set or changed as needed.

### Acceptance Criteria

```gherkin
Given an item exists with no urgency level assigned
When I assign urgency level 3 to that item
Then the item's urgency level is set to 3
```

**UML class diagram:** `experiments/project_8/class_diagram_54.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/patient/Patient.py` | `Permission` |
| `src/domain/urgency_level/UrgencyLevel.py` | `Actor`, `IfaceKind`, `Interface`, `Permission`, `Resource`, `State`, `UrgencyLevel` |
| `src/repository/urgency_level/urgency_level_repository.py` | `Item_Management_API` |
| `src/service/urgency_level/urgency_level_service.py` | `REQ_ITEM_URGENCY_01` |

---

### Task #55 — Order queue by urgency then time

**As a** user
**I need** the system to order the queue by urgency then time
**So that** I can address the most urgent items first and maintain chronological order within same urgency

### Details and Assumptions
* The queue contains items, each with an urgency level and a timestamp.
* "Urgency" implies a priority value (e.g., high, medium, low) and sorting is descending (highest urgency first).
* "Time" refers to the creation or submission time, and sorting is ascending (oldest first).

### Acceptance Criteria

```gherkin
Given there is a queue with items of varying urgencies and timestamps
When the queue is ordered by urgency then time
Then the items are sorted first by urgency (highest to lowest) and then by time (oldest to newest)
```

**UML class diagram:** `experiments/project_8/class_diagram_55.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/queue/Queue.py` | `Queue`, `QueueItem` |
| `src/domain/urgency_level/UrgencyLevel.py` | `UrgencyLevel` |

---

### Task #56 — Reorder queue on change

**As a** user
**I need** the system to reorder the queue when a change occurs
**So that** the queue reflects the updated order based on the change

### Details and Assumptions
* The system automatically reorders the queue when a change is detected.
* The change could be an addition, removal, or modification of an item in the queue.

### Acceptance Criteria

```gherkin
Given the queue has items in a specific order
When a change is made to the queue
Then the queue is automatically reordered according to the defined rules
```

**UML class diagram:** `experiments/project_8/class_diagram_56.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/patient/Patient.py` | `Permission` |
| `src/domain/queue/Queue.py` | `Queue`, `QueueItem` |
| `src/domain/urgency_level/UrgencyLevel.py` | `Actor`, `Permission`, `Resource`, `State` |

---

### Task #57 — Take next patient from head

**As a** healthcare practitioner  
**I need** to take the next patient from the head of the queue  
**So that** patients are seen in order of arrival

### Details and Assumptions
* There is a queue of waiting patients.
* "Head" refers to the first patient in the queue.
* The system should automatically provide the next patient when requested.

### Acceptance Criteria

```gherkin
Given there is a queue with multiple patients
When the practitioner requests to take the next patient
Then the system displays the patient at the head of the queue
And removes that patient from the queue
```

**UML class diagram:** `experiments/project_8/class_diagram_57.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/patient/Patient.py` | `Patient`, `Permission` |
| `src/domain/queue/Queue.py` | `Queue` |
| `src/domain/urgency_level/UrgencyLevel.py` | `Permission` |

---

### Task #58 — Live dashboard with urgency and wait time

**As a** user
**I need** a live dashboard that displays urgency and wait time
**So that** I can prioritize tasks based on current urgency and waiting duration

### Details and Assumptions
* The dashboard updates in real time.
* Urgency and wait time data are available from the system.
* The user has access to view the dashboard.

### Acceptance Criteria

```gherkin
Given I am on the live dashboard
When urgency and wait time data are updated
Then the dashboard shows the current urgency and wait time values
```

**UML class diagram:** `experiments/project_8/class_diagram_58.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/patient/Patient.py` | `Patient`, `Permission` |
| `src/domain/queue/Queue.py` | `Queue` |
| `src/domain/urgency_level/UrgencyLevel.py` | `Actor`, `IfaceKind`, `Interface`, `Permission`, `Resource`, `State`, `UrgencyLevel` |

---
