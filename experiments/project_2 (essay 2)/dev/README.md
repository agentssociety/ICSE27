# Project 6 — Scaffold Reference

Auto-generated from the persisted package design, requirement artifacts, and UML diagrams.
Intended as a navigation aid for follow-up agents and developers.

---

## Statistics

| Item | Count |
|------|-------|
| Packages | 27 |
| Requirements linked | 7 |
| Tasks | 7 |
| Domain classes | 3 |

---

## Notes

- Generated files are implementation skeletons intended to be filled in by follow-up agents or developers.
- Existing files are preserved unless `overwrite_existing=True` is used.

---

## File Index

All generated files organised by package.

### `domain.blood_unit` · layer: `domain`

Path: `src/domain/blood_unit`
> Domain layer for the BloodUnit domain class

| File | Classes |
|------|---------|
| `BloodUnit.py` | `Permission`, `ABOType`, `RhFactor`, `BloodUnitStatus`, `State`, `Actor`, `BloodUnit`, `Resource`, `BloodUnitId`, `BloodUnitCreatedEvent`, `BloodUnitUpdatedEvent` |

### `dto.blood_unit` · layer: `dto`

Path: `src/dto/blood_unit`
> Dto layer for the BloodUnit domain class

| File | Classes |
|------|---------|
| `blood_unit_dto.py` | `BloodUnitCreateRequest`, `BloodUnitUpdateRequest`, `BloodUnitResponse` |

### `repository.blood_unit` · layer: `repository`

Path: `src/repository/blood_unit`
> Repository layer for the BloodUnit domain class

| File | Classes |
|------|---------|
| `blood_unit_repository.py` | `Interface`, `BloodUnitDatabase`, `InventoryManagementUI` |

### `orm.blood_unit` · layer: `orm`

Path: `src/orm/blood_unit`
> Orm layer for the BloodUnit domain class

| File | Classes |
|------|---------|
| `blood_unit_orm.py` | `BloodUnitORM` |

### `infra.blood_unit` · layer: `infra`

Path: `src/infra/blood_unit`
> Infra layer for the BloodUnit domain class

| File | Classes |
|------|---------|
| `blood_unit_repo_impl.py` | `SQLAlchemyBloodUnitRepository` |

### `service.blood_unit` · layer: `service`

Path: `src/service/blood_unit`
> Service layer for the BloodUnit domain class

| File | Classes |
|------|---------|
| `blood_unit_service.py` | `BloodUnitService`, `BloodUnitServiceImpl` |

### `api.blood_unit` · layer: `api`

Path: `src/api/blood_unit`
> Api layer for the BloodUnit domain class

| File | Classes |
|------|---------|
| `blood_unit_router.py` | `BloodUnitRouter` |

### `tests.unit.blood_unit` · layer: `tests`

Path: `tests/unit/blood_unit`
> Unit tests for BloodUnit across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_blood_unit_domain.py` | — |
| `test_blood_unit_service.py` | — |
| `test_blood_unit_api.py` | — |

### `domain.transfusion_request` · layer: `domain`

Path: `src/domain/transfusion_request`
> Domain layer for the TransfusionRequest domain class

| File | Classes |
|------|---------|
| `TransfusionRequest.py` | `TransfusionRequest`, `BloodType`, `RhFactor`, `Inventory`, `Permission`, `RequestState`, `TransfusionRequestId`, `TransfusionRequestCreatedEvent`, `TransfusionRequestUpdatedEvent` |

### `dto.transfusion_request` · layer: `dto`

Path: `src/dto/transfusion_request`
> Dto layer for the TransfusionRequest domain class

| File | Classes |
|------|---------|
| `transfusion_request_dto.py` | `TransfusionRequestDTO`, `ValidationResult`, `StorageResult`, `Response` |

### `repository.transfusion_request` · layer: `repository`

Path: `src/repository/transfusion_request`
> Repository layer for the TransfusionRequest domain class

| File | Classes |
|------|---------|
| `transfusion_request_repository.py` | `TransfusionRequestSubmissionAPI`, `TransfusionRequestDatabase` |

### `orm.transfusion_request` · layer: `orm`

Path: `src/orm/transfusion_request`
> Orm layer for the TransfusionRequest domain class

| File | Classes |
|------|---------|
| `transfusion_request_orm.py` | `TransfusionRequestORM` |

### `infra.transfusion_request` · layer: `infra`

Path: `src/infra/transfusion_request`
> Infra layer for the TransfusionRequest domain class

| File | Classes |
|------|---------|
| `transfusion_request_repo_impl.py` | `SQLAlchemyTransfusionRequestRepository` |

### `service.transfusion_request` · layer: `service`

Path: `src/service/transfusion_request`
> Service layer for the TransfusionRequest domain class

| File | Classes |
|------|---------|
| `transfusion_request_service.py` | `BloodBankStaff`, `ClinicalTeams`, `Patients` |

### `api.transfusion_request` · layer: `api`

Path: `src/api/transfusion_request`
> Api layer for the TransfusionRequest domain class

| File | Classes |
|------|---------|
| `transfusion_request_router.py` | `TransfusionRequestRouter` |

### `tests.unit.transfusion_request` · layer: `tests`

Path: `tests/unit/transfusion_request`
> Unit tests for TransfusionRequest across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_transfusion_request_domain.py` | — |
| `test_transfusion_request_service.py` | — |
| `test_transfusion_request_api.py` | — |

### `domain.reservation` · layer: `domain`

Path: `src/domain/reservation`
> Domain layer for the Reservation domain class

| File | Classes |
|------|---------|
| `Reservation.py` | `BloodUnitStatus`, `TransfusionRequestStatus`, `ReservationStatus`, `BloodType`, `Role`, `Permission`, `Reservation`, `ReservationId`, `ReservationCreatedEvent`, `ReservationUpdatedEvent` |

### `dto.reservation` · layer: `dto`

Path: `src/dto/reservation`
> Dto layer for the Reservation domain class

| File | Classes |
|------|---------|
| `reservation_dto.py` | `ReservationRequestDTO`, `ReservationResponseDTO` |

### `repository.reservation` · layer: `repository`

Path: `src/repository/reservation`
> Repository layer for the Reservation domain class

| File | Classes |
|------|---------|
| `reservation_repository.py` | `BloodInventoryDatabase`, `ReservationReleaseScheduler`, `AdminDashboard`, `BloodTypeCompatibilityAlgorithm` |

### `orm.reservation` · layer: `orm`

Path: `src/orm/reservation`
> Orm layer for the Reservation domain class

| File | Classes |
|------|---------|
| `reservation_orm.py` | `ReservationORM` |

### `infra.reservation` · layer: `infra`

Path: `src/infra/reservation`
> Infra layer for the Reservation domain class

| File | Classes |
|------|---------|
| `reservation_repo_impl.py` | `SQLAlchemyReservationRepository` |

### `service.reservation` · layer: `service`

Path: `src/service/reservation`
> Service layer for the Reservation domain class

| File | Classes |
|------|---------|
| `reservation_service.py` | `ReservationService`, `ReservationServiceImpl` |

### `api.reservation` · layer: `api`

Path: `src/api/reservation`
> Api layer for the Reservation domain class

| File | Classes |
|------|---------|
| `reservation_router.py` | `ReservationAPI` |

### `tests.unit.reservation` · layer: `tests`

Path: `tests/unit/reservation`
> Unit tests for Reservation across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_reservation_domain.py` | — |
| `test_reservation_service.py` | — |
| `test_reservation_api.py` | — |

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
| `test_blood_unit_flow.py` | — |
| `test_transfusion_request_flow.py` | — |
| `test_reservation_flow.py` | — |
| `test_api_contracts.py` | — |
| `conftest.py` | — |

---

## Task Index

For each task: full description, files whose classes appear in the task's UML diagram,
and paths to the linked requirement specification and UML diagrams.

### Task #32 — Blood Unit Tracking System

**As a** blood bank manager
**I need** to track blood units by ABO type, Rh factor, collection date, and enforce 42-day expiry, with each unit uniquely identified and its status tracked throughout its lifecycle
**So that** I can ensure blood inventory is safe, traceable, and compliant with expiration regulations

### Details and Assumptions
* Each blood unit has a unique identifier (e.g., barcode or serial number).
* ABO type and Rh factor are recorded at collection.
* Collection date is used to calculate the 42-day expiry date.
* Status includes stages such as collected, tested, available, issued, or expired.
* The system should automatically flag or remove expired units.

### Acceptance Criteria

```gherkin
Given a blood unit is collected with a unique ID, ABO type, Rh factor, and collection date
When the collection date is recorded
Then the system calculates the expiry date as 42 days from collection

Given a blood unit is in inventory
When its status changes (e.g., from available to issued)
Then the system updates the unit's status and logs the change

Given a blood unit's expiry date has passed
When the system checks inventory
Then the unit is marked as expired and is no longer available for use
```

**UML class diagram:** `experiments/project_6/class_diagram_32.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/blood_unit/BloodUnit.py` | `ABOType`, `Actor`, `BloodUnit`, `BloodUnitStatus`, `Permission`, `Resource`, `RhFactor`, `State` |
| `src/domain/reservation/Reservation.py` | `BloodUnitStatus`, `Permission` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `Permission`, `RhFactor` |
| `src/repository/blood_unit/blood_unit_repository.py` | `BloodUnitDatabase`, `Interface`, `InventoryManagementUI` |

---

### Task #33 — Transfusion Request Intake

**As a** blood bank staff member
**I need** to accept transfusion requests specifying required blood type, Rh factor, and quantity, and validate request parameters and store them for matching against available inventory
**So that** requests can be accurately processed and matched with available blood supply

### Details and Assumptions
* The system will accept transfusion requests with blood type, Rh factor, and quantity fields
* Request parameters will be validated for correctness and completeness
* Validated requests will be stored in a database for later matching against inventory

### Acceptance Criteria

```gherkin
Given a transfusion request with blood type, Rh factor, and quantity
When the request parameters are validated
Then the request is stored for matching against available inventory

Given a transfusion request with missing or invalid parameters
When the request parameters are validated
Then an error is returned and the request is not stored
```

**UML class diagram:** `experiments/project_6/class_diagram_33.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/blood_unit/BloodUnit.py` | `Permission`, `RhFactor` |
| `src/domain/reservation/Reservation.py` | `BloodType`, `Permission` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `BloodType`, `Inventory`, `Permission`, `RequestState`, `RhFactor`, `TransfusionRequest` |
| `src/dto/transfusion_request/transfusion_request_dto.py` | `Response`, `StorageResult`, `TransfusionRequestDTO`, `ValidationResult` |
| `src/repository/transfusion_request/transfusion_request_repository.py` | `TransfusionRequestDatabase`, `TransfusionRequestSubmissionAPI` |
| `src/service/transfusion_request/transfusion_request_service.py` | `BloodBankStaff`, `ClinicalTeams`, `Patients` |

---

### Task #34 — Blood Unit Matching Algorithm

**As a** blood bank technician
**I need** to match transfusion requests to compatible blood units, prioritizing exact ABO/Rh type matches first, then selecting units with the closest expiry date among compatible types
**So that** I can ensure only valid cross-matches are considered and maximize unit utilization

### Details and Assumptions
* The system has access to blood unit inventory with ABO/Rh type, expiry date, and cross-match status
* Compatible types include exact matches and other types that are cross-match compatible
* Prioritization is: 1) exact ABO/Rh match, 2) closest expiry date among compatible types
* Only units that have passed valid cross-matching are considered

### Acceptance Criteria

```gherkin
Given a transfusion request for a specific ABO/Rh type
When matching blood units are searched
Then the system should first return units with exact ABO/Rh match sorted by closest expiry date

Given a transfusion request with no exact ABO/Rh match available
When compatible types are considered
Then the system should select units with the closest expiry date among compatible types

Given a blood unit that has not passed cross-match validation
When matching units are evaluated
Then that unit should be excluded from the results
```

**UML class diagram:** `experiments/project_6/class_diagram_34.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/blood_unit/BloodUnit.py` | `BloodUnit` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `TransfusionRequest` |

---

### Task #35 — Unit Reservation and Auto-Release

**As a** blood bank system
**I need** to automatically reserve matched blood units for pending transfusion requests and release reservations after 24 hours if not issued
**So that** units are not unnecessarily held and can be made available for other urgent requests

### Details and Assumptions
* Reservations are made based on blood type and compatibility matching
* The 24-hour release timer starts from the time of reservation
* Released units become immediately available for other requests

### Acceptance Criteria

```gherkin
Given a blood unit is reserved for a pending transfusion request
When 24 hours have elapsed without the unit being issued
Then the reservation is automatically released and the unit is marked as available for other requests
```

**UML class diagram:** `experiments/project_6/class_diagram_35.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/reservation/reservation_router.py` | `ReservationAPI` |
| `src/domain/blood_unit/BloodUnit.py` | `BloodUnit`, `BloodUnitStatus`, `Permission` |
| `src/domain/reservation/Reservation.py` | `BloodType`, `BloodUnitStatus`, `Permission`, `Reservation`, `ReservationStatus`, `Role`, `TransfusionRequestStatus` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `BloodType`, `Permission`, `TransfusionRequest` |
| `src/dto/reservation/reservation_dto.py` | `ReservationRequestDTO`, `ReservationResponseDTO` |
| `src/repository/reservation/reservation_repository.py` | `AdminDashboard`, `BloodInventoryDatabase`, `BloodTypeCompatibilityAlgorithm`, `ReservationReleaseScheduler` |

---

### Task #36 — Automatic Unit Expiration

**As a** inventory manager
**I need** the system to automatically mark blood units as expired after 42 days
**So that** expired units are removed from available inventory and their status is updated accordingly

### Details and Assumptions
* Blood units have a standard shelf life of 42 days.
* The system should automatically check expiration based on the collection date.
* Expired units should be removed from the available inventory pool.

### Acceptance Criteria

```gherkin
Given a blood unit with a collection date over 42 days ago
When the system checks the inventory status
Then the blood unit is marked as expired
And the blood unit is removed from available inventory
And the unit's status is updated to "expired"
```

**UML class diagram:** `experiments/project_6/class_diagram_36.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/blood_unit/BloodUnit.py` | `Actor`, `BloodUnit`, `BloodUnitStatus`, `Permission`, `Resource`, `State` |
| `src/domain/reservation/Reservation.py` | `BloodUnitStatus`, `Permission` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `Inventory`, `Permission` |
| `src/repository/blood_unit/blood_unit_repository.py` | `Interface` |

---

### Task #37 — Stock Shortage Alert System

**As a** blood bank manager
**I need** to monitor blood inventory levels per ABO/Rh type and be alerted when stock for any blood type falls below 5 units
**So that** I can notify relevant personnel to initiate restocking procedures

### Details and Assumptions
* The system tracks inventory units for each ABO/Rh blood type.
* The alert threshold is defined as 5 units for any blood type.
* Notifications are sent to designated personnel (e.g., procurement team).

### Acceptance Criteria

```gherkin
Given the blood bank inventory tracking system is active
When the stock level for any ABO/Rh blood type drops below 5 units
Then the system raises an alert
And relevant personnel are notified to initiate restocking
```

**UML class diagram:** `experiments/project_6/class_diagram_37.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/blood_unit/BloodUnit.py` | `Resource`, `State` |
| `src/domain/reservation/Reservation.py` | `BloodType` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `BloodType` |

---

### Task #38 — Blood Bank Dashboard

**As a** blood bank manager
**I need** a dashboard displaying current stock levels per ABO/Rh type, units nearing expiration, and open transfusion requests
**So that** I can have a quick visual overview of blood bank status

### Details and Assumptions
* Dashboard is digital, updated in real time, and accessible from standard devices.
* Data sources include inventory system (stock levels, expiration dates) and transfusion request system.
* Dashboard is designed for at-a-glance reading, with visual highlights for critical items.

### Acceptance Criteria

```gherkin
Given the blood bank has current inventory data, units nearing expiration, and open transfusion requests
When the blood bank manager accesses the dashboard
Then the dashboard displays current stock levels per ABO/Rh type, highlights units nearing expiration, and lists open transfusion requests
```

**UML class diagram:** `experiments/project_6/class_diagram_38.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/blood_unit/BloodUnit.py` | `Permission` |
| `src/domain/reservation/Reservation.py` | `Permission` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `Permission`, `TransfusionRequest` |

---
