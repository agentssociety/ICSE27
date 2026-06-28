# Project 5 — Scaffold Reference

Auto-generated from the persisted package design, requirement artifacts, and UML diagrams.
Intended as a navigation aid for follow-up agents and developers.

---

## Statistics

| Item | Count |
|------|-------|
| Packages | 35 |
| Requirements linked | 7 |
| Tasks | 7 |
| Domain classes | 4 |

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
| `BloodUnit.py` | `ABO`, `Rh`, `BloodUnit`, `BloodUnitId`, `BloodUnitCreatedEvent`, `BloodUnitUpdatedEvent` |

### `dto.blood_unit` · layer: `dto`

Path: `src/dto/blood_unit`
> Dto layer for the BloodUnit domain class

| File | Classes |
|------|---------|
| `blood_unit_dto.py` | `RecordBloodUnitRequest`, `BloodUnitResponse` |

### `repository.blood_unit` · layer: `repository`

Path: `src/repository/blood_unit`
> Repository layer for the BloodUnit domain class

| File | Classes |
|------|---------|
| `blood_unit_repository.py` | `BloodUnitDB`, `DateCalculationAPI` |

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
| `blood_unit_service.py` | `BloodUnitService` |

### `api.blood_unit` · layer: `api`

Path: `src/api/blood_unit`
> Api layer for the BloodUnit domain class

| File | Classes |
|------|---------|
| `blood_unit_router.py` | `BloodUnitController` |

### `tests.unit.blood_unit` · layer: `tests`

Path: `tests/unit/blood_unit`
> Unit tests for BloodUnit across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_blood_unit_domain.py` | — |
| `test_blood_unit_service.py` | — |
| `test_blood_unit_api.py` | — |

### `domain.alert` · layer: `domain`

Path: `src/domain/alert`
> Domain layer for the Alert domain class

| File | Classes |
|------|---------|
| `Alert.py` | `Permission`, `State`, `User`, `Resource`, `BloodTypeResource`, `Operation`, `BloodTypeAlertOperation`, `Alert`, `AlertId`, `AlertCreatedEvent`, `AlertUpdatedEvent` |

### `dto.alert` · layer: `dto`

Path: `src/dto/alert`
> Dto layer for the Alert domain class

| File | Classes |
|------|---------|
| `alert_dto.py` | `AlertRequest`, `InventoryLevel`, `OperationRequest` |

### `repository.alert` · layer: `repository`

Path: `src/repository/alert`
> Repository layer for the Alert domain class

| File | Classes |
|------|---------|
| `alert_repository.py` | `Channel`, `InventoryPort`, `NotificationPort` |

### `orm.alert` · layer: `orm`

Path: `src/orm/alert`
> Orm layer for the Alert domain class

| File | Classes |
|------|---------|
| `alert_orm.py` | `AlertORM` |

### `infra.alert` · layer: `infra`

Path: `src/infra/alert`
> Infra layer for the Alert domain class

| File | Classes |
|------|---------|
| `alert_repo_impl.py` | `SQLAlchemyAlertRepository` |

### `service.alert` · layer: `service`

Path: `src/service/alert`
> Service layer for the Alert domain class

| File | Classes |
|------|---------|
| `alert_service.py` | `AlertService` |

### `api.alert` · layer: `api`

Path: `src/api/alert`
> Api layer for the Alert domain class

| File | Classes |
|------|---------|
| `alert_router.py` | `InventoryApiAdapter`, `NotificationGatewayAdapter` |

### `tests.unit.alert` · layer: `tests`

Path: `tests/unit/alert`
> Unit tests for Alert across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_alert_domain.py` | — |
| `test_alert_service.py` | — |
| `test_alert_api.py` | — |

### `domain.reservation` · layer: `domain`

Path: `src/domain/reservation`
> Domain layer for the Reservation domain class

| File | Classes |
|------|---------|
| `Reservation.py` | `Permission`, `IfaceKind`, `State`, `Actor`, `Resource`, `Interface`, `Scheduling_API`, `Blood_Inventory_Database`, `REQ_BB_01`, `CancellationRecord`, `OverlapRecord`, `OutageRecord`, `Reservation`, `ReservationId`, `ReservationCreatedEvent`, `ReservationUpdatedEvent` |

### `dto.reservation` · layer: `dto`

Path: `src/dto/reservation`
> Dto layer for the Reservation domain class

| File | Classes |
|------|---------|
| `reservation_dto.py` | `ReservationCreateRequest`, `ReservationUpdateRequest`, `ReservationResponse` |

### `repository.reservation` · layer: `repository`

Path: `src/repository/reservation`
> Repository layer for the Reservation domain class

| File | Classes |
|------|---------|
| `reservation_repository.py` | `ReservationRepository` |

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
| `reservation_router.py` | `ReservationRouter` |

### `tests.unit.reservation` · layer: `tests`

Path: `tests/unit/reservation`
> Unit tests for Reservation across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_reservation_domain.py` | — |
| `test_reservation_service.py` | — |
| `test_reservation_api.py` | — |

### `domain.transfusion_request` · layer: `domain`

Path: `src/domain/transfusion_request`
> Domain layer for the TransfusionRequest domain class

| File | Classes |
|------|---------|
| `TransfusionRequest.py` | `TransfusionRequest`, `PatientDetails`, `BloodType`, `Quantity`, `Urgency`, `UniqueID`, `StateEnum`, `Permission`, `TransfusionRequestId`, `TransfusionRequestCreatedEvent`, `TransfusionRequestUpdatedEvent` |

### `dto.transfusion_request` · layer: `dto`

Path: `src/dto/transfusion_request`
> Dto layer for the TransfusionRequest domain class

| File | Classes |
|------|---------|
| `transfusion_request_dto.py` | `TransfusionRequestCreateRequest`, `TransfusionRequestUpdateRequest`, `TransfusionRequestResponse` |

### `repository.transfusion_request` · layer: `repository`

Path: `src/repository/transfusion_request`
> Repository layer for the TransfusionRequest domain class

| File | Classes |
|------|---------|
| `transfusion_request_repository.py` | `TransfusionRequestAPI`, `TransfusionRequestDB` |

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
| `transfusion_request_service.py` | `HealthcareProvider`, `BloodBankTechnician`, `IT_Team` |

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
| `test_alert_flow.py` | — |
| `test_api_contracts.py` | — |
| `conftest.py` | — |

---

## Task Index

For each task: full description, files whose classes appear in the task's UML diagram,
and paths to the linked requirement specification and UML diagrams.

### Task #25 — Blood Unit Tracking

**As a** inventory manager  
**I need** to track blood units by type, Rh factor, and donation date  
**So that** I can ensure proper matching and expiration management  

### Details and Assumptions  
* Blood units are categorized by type (e.g., A, B, AB, O) and Rh factor (positive/negative)  
* Donation date is recorded for each unit to monitor shelf life  

### Acceptance Criteria  

```gherkin
Given a blood unit is received  
When the unit is logged into the system  
Then its blood type, Rh factor, and donation date are recorded  

Given a blood unit with a known donation date  
When the expiration date is calculated  
Then the system can flag units near or past expiration  
```

**UML class diagram:** `experiments/project_5/class_diagram_25.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/blood_unit/blood_unit_router.py` | `BloodUnitController` |
| `src/domain/alert/Alert.py` | `Permission` |
| `src/domain/blood_unit/BloodUnit.py` | `ABO`, `BloodUnit`, `Rh` |
| `src/domain/reservation/Reservation.py` | `Actor`, `Permission` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `Permission` |
| `src/dto/blood_unit/blood_unit_dto.py` | `BloodUnitResponse`, `RecordBloodUnitRequest` |
| `src/repository/blood_unit/blood_unit_repository.py` | `BloodUnitDB`, `DateCalculationAPI` |
| `src/service/blood_unit/blood_unit_service.py` | `BloodUnitService` |

---

### Task #26 — Transfusion Request Acceptance

**As a** blood bank technician
**I need** accept and log transfusion requests from healthcare providers
**So that** we can process and track transfusion requests efficiently

### Details and Assumptions
* Transfusion requests come from healthcare providers (e.g., hospitals, clinics).
* Each request includes patient details, blood type, quantity, and urgency.
* Logging stores the request in a database with a unique identifier for tracking.

### Acceptance Criteria

```gherkin
Given a healthcare provider submits a transfusion request
When the request is received by the system
Then the request is accepted and logged in the database with a unique ID
```

**UML class diagram:** `experiments/project_5/class_diagram_26.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/alert/Alert.py` | `Permission` |
| `src/domain/reservation/Reservation.py` | `Permission` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `BloodType`, `PatientDetails`, `Permission`, `Quantity`, `StateEnum`, `TransfusionRequest`, `UniqueID`, `Urgency` |
| `src/repository/transfusion_request/transfusion_request_repository.py` | `TransfusionRequestAPI`, `TransfusionRequestDB` |
| `src/service/transfusion_request/transfusion_request_service.py` | `BloodBankTechnician`, `HealthcareProvider`, `IT_Team` |

---

### Task #27 — Compatibility Matching

**As a** lab technician
**I need** to match transfusion requests to compatible blood units based on type and Rh factor
**So that** patients receive safe transfusions

### Details and Assumptions
* The matching considers ABO blood group and Rh factor compatibility.
* Only units with identical or compatible type and Rh factor are suggested.
* Incompatible matches are excluded.

### Acceptance Criteria

```gherkin
Given a transfusion request for blood type A positive
When the system searches for compatible blood units
Then it returns only units that are A positive or O positive
```

**UML class diagram:** `experiments/project_5/class_diagram_27.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/blood_unit/BloodUnit.py` | `BloodUnit` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `TransfusionRequest` |

---

### Task #28 — Reservation and Auto-Release

**As a** blood bank manager
**I need** units to be reserved for scheduled transfusions and automatically released if not used within a timeframe
**So that** blood products are available for scheduled patients without being wasted if unused

### Details and Assumptions
* The system supports scheduling transfusions in advance.
* A defined timeframe (e.g., hours or days) for unit release is configured.
* Units are reserved only for confirmed scheduled transfusions.
* Automatic release occurs once the timeframe expires without usage.

### Acceptance Criteria

```gherkin
Given a scheduled transfusion with reserved units
When the scheduled time passes without the units being used
Then the reservation is automatically released
```

**UML class diagram:** `experiments/project_5/class_diagram_28.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/alert/Alert.py` | `Permission`, `Resource`, `State` |
| `src/domain/reservation/Reservation.py` | `Actor`, `Blood_Inventory_Database`, `CancellationRecord`, `IfaceKind`, `Interface`, `OutageRecord`, `OverlapRecord`, `Permission`, `REQ_BB_01`, `Resource`, `Scheduling_API`, `State` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `Permission` |

---

### Task #29 — Automatic Expiration

**As a** blood bank administrator
**I need** blood units older than 42 days to be automatically expired
**So that** outdated blood is not mistakenly used for transfusions

### Details and Assumptions
* Blood units have a maximum shelf life of 42 days.
* The system should automatically flag or deactivate units that exceed this age.
* This reduces manual checking and human error.

### Acceptance Criteria

```gherkin
Given a blood unit has a collection date
When the current date is more than 42 days after the collection date
Then the blood unit is automatically marked as expired
```

**UML class diagram:** `experiments/project_5/class_diagram_29.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/blood_unit/BloodUnit.py` | `BloodUnit` |

---

### Task #30 — Shortage Alert

**As a** blood bank manager
**I need** the system to raise an alert when stock of any blood type drops below 5 units
**So that** I can replenish supplies before a shortage occurs

### Details and Assumptions
* The system tracks inventory levels for each blood type (A+, A-, B+, B-, AB+, AB-, O+, O-).
* The threshold for triggering an alert is 5 units.
* Alerts can be sent via email, SMS, or in-app notification.

### Acceptance Criteria

```gherkin
Given the blood bank has inventory levels for each blood type
When the stock of any blood type falls below 5 units
Then the system raises an alert to notify the blood bank manager
```

**UML class diagram:** `experiments/project_5/class_diagram_30.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/alert/alert_router.py` | `InventoryApiAdapter`, `NotificationGatewayAdapter` |
| `src/domain/alert/Alert.py` | `BloodTypeAlertOperation`, `BloodTypeResource`, `Permission`, `State`, `User` |
| `src/domain/reservation/Reservation.py` | `Permission`, `State` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `Permission` |
| `src/dto/alert/alert_dto.py` | `AlertRequest`, `InventoryLevel`, `OperationRequest` |
| `src/repository/alert/alert_repository.py` | `Channel`, `NotificationPort` |
| `src/service/alert/alert_service.py` | `AlertService` |

---

### Task #31 — Dashboard

**As a** inventory manager
**I need** a dashboard that shows current stock levels, expiring units, and pending requests
**So that** I can monitor inventory health, prioritize actions to reduce waste, and respond to urgent needs

### Details and Assumptions
* The dashboard is a single view consolidating three key data points: stock, expiration, and requests.
* It is intended for daily or shift-based monitoring.
* Users have access to a system with inventory and request data.

### Acceptance Criteria

```gherkin
Given I am on the inventory dashboard
When I view the summary section
Then I see current stock levels for each item
And I see a list of units approaching expiration
And I see a count of pending requests
```

**UML class diagram:** `experiments/project_5/class_diagram_31.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/alert/Alert.py` | `Permission`, `Resource`, `State` |
| `src/domain/reservation/Reservation.py` | `Actor`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `Permission` |

---
