# Project 9 — Scaffold Reference

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

### `domain.flight` · layer: `domain`

Path: `src/domain/flight`
> Domain layer for the Flight domain class

| File | Classes |
|------|---------|
| `Flight.py` | `Flight`, `Resource`, `Permission`, `State`, `FlightType`, `FlightStatus`, `FlightId`, `FlightCreatedEvent`, `FlightUpdatedEvent` |

### `dto.flight` · layer: `dto`

Path: `src/dto/flight`
> Dto layer for the Flight domain class

| File | Classes |
|------|---------|
| `flight_dto.py` | `FlightRegistrationRequest`, `FlightUpdateRequest` |

### `repository.flight` · layer: `repository`

Path: `src/repository/flight`
> Repository layer for the Flight domain class

| File | Classes |
|------|---------|
| `flight_repository.py` | `FlightRegistrationAPI`, `FlightDataStore`, `FlightManagementDashboard` |

### `orm.flight` · layer: `orm`

Path: `src/orm/flight`
> Orm layer for the Flight domain class

| File | Classes |
|------|---------|
| `flight_orm.py` | `FlightORM` |

### `infra.flight` · layer: `infra`

Path: `src/infra/flight`
> Infra layer for the Flight domain class

| File | Classes |
|------|---------|
| `flight_repo_impl.py` | `SQLAlchemyFlightRepository` |

### `service.flight` · layer: `service`

Path: `src/service/flight`
> Service layer for the Flight domain class

| File | Classes |
|------|---------|
| `flight_service.py` | `FlightService` |

### `api.flight` · layer: `api`

Path: `src/api/flight`
> Api layer for the Flight domain class

| File | Classes |
|------|---------|
| `flight_router.py` | `AirTrafficController`, `FlightOperationsTeam` |

### `tests.unit.flight` · layer: `tests`

Path: `tests/unit/flight`
> Unit tests for Flight across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_flight_domain.py` | — |
| `test_flight_service.py` | — |
| `test_flight_api.py` | — |

### `domain.time_slot` · layer: `domain`

Path: `src/domain/time_slot`
> Domain layer for the TimeSlot domain class

| File | Classes |
|------|---------|
| `TimeSlot.py` | `TimeSlot`, `TimeSlotId`, `TimeSlotCreatedEvent`, `TimeSlotUpdatedEvent` |

### `dto.time_slot` · layer: `dto`

Path: `src/dto/time_slot`
> Dto layer for the TimeSlot domain class

| File | Classes |
|------|---------|
| `time_slot_dto.py` | `TimeSlotCreateRequest`, `TimeSlotUpdateRequest`, `TimeSlotResponse` |

### `repository.time_slot` · layer: `repository`

Path: `src/repository/time_slot`
> Repository layer for the TimeSlot domain class

| File | Classes |
|------|---------|
| `time_slot_repository.py` | `TimeSlotRepository` |

### `orm.time_slot` · layer: `orm`

Path: `src/orm/time_slot`
> Orm layer for the TimeSlot domain class

| File | Classes |
|------|---------|
| `time_slot_orm.py` | `TimeSlotORM` |

### `infra.time_slot` · layer: `infra`

Path: `src/infra/time_slot`
> Infra layer for the TimeSlot domain class

| File | Classes |
|------|---------|
| `time_slot_repo_impl.py` | `SQLAlchemyTimeSlotRepository` |

### `service.time_slot` · layer: `service`

Path: `src/service/time_slot`
> Service layer for the TimeSlot domain class

| File | Classes |
|------|---------|
| `time_slot_service.py` | `TimeSlotService`, `TimeSlotServiceImpl` |

### `api.time_slot` · layer: `api`

Path: `src/api/time_slot`
> Api layer for the TimeSlot domain class

| File | Classes |
|------|---------|
| `time_slot_router.py` | `TimeSlotRouter` |

### `tests.unit.time_slot` · layer: `tests`

Path: `tests/unit/time_slot`
> Unit tests for TimeSlot across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_time_slot_domain.py` | — |
| `test_time_slot_service.py` | — |
| `test_time_slot_api.py` | — |

### `domain.runway` · layer: `domain`

Path: `src/domain/runway`
> Domain layer for the Runway domain class

| File | Classes |
|------|---------|
| `Runway.py` | `Runway`, `Slot`, `AlternativeRunway`, `Operation`, `Resource`, `Channel`, `Interface`, `RunwayId`, `RunwayCreatedEvent`, `RunwayUpdatedEvent` |

### `dto.runway` · layer: `dto`

Path: `src/dto/runway`
> Dto layer for the Runway domain class

| File | Classes |
|------|---------|
| `runway_dto.py` | `RunwayCreateRequest`, `RunwayUpdateRequest`, `RunwayResponse` |

### `repository.runway` · layer: `repository`

Path: `src/repository/runway`
> Repository layer for the Runway domain class

| File | Classes |
|------|---------|
| `runway_repository.py` | `FlightSchedulingAPI`, `RunwayStatusDatabase`, `AirTrafficControlConsole` |

### `orm.runway` · layer: `orm`

Path: `src/orm/runway`
> Orm layer for the Runway domain class

| File | Classes |
|------|---------|
| `runway_orm.py` | `RunwayORM` |

### `infra.runway` · layer: `infra`

Path: `src/infra/runway`
> Infra layer for the Runway domain class

| File | Classes |
|------|---------|
| `runway_repo_impl.py` | `SQLAlchemyRunwayRepository` |

### `service.runway` · layer: `service`

Path: `src/service/runway`
> Service layer for the Runway domain class

| File | Classes |
|------|---------|
| `runway_service.py` | `Actor`, `AirTrafficControl`, `FlightOperations`, `Passengers`, `Permission` |

### `api.runway` · layer: `api`

Path: `src/api/runway`
> Api layer for the Runway domain class

| File | Classes |
|------|---------|
| `runway_router.py` | `RunwayRouter` |

### `tests.unit.runway` · layer: `tests`

Path: `tests/unit/runway`
> Unit tests for Runway across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_runway_domain.py` | — |
| `test_runway_service.py` | — |
| `test_runway_api.py` | — |

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
| `test_flight_flow.py` | — |
| `test_time_slot_flow.py` | — |
| `test_runway_flow.py` | — |
| `test_api_contracts.py` | — |
| `conftest.py` | — |

---

## Task Index

For each task: full description, files whose classes appear in the task's UML diagram,
and paths to the linked requirement specification and UML diagrams.

### Task #65 — Flight Registration

**As a** air traffic controller
**I need** to register incoming and outgoing flights
**So that** all flight operations are recorded and managed within the system

### Details and Assumptions
* The system supports flight registration with fields: flight number, airline, origin/destination, scheduled time, and type (arrival/departure)
* Registered flights can be edited or cancelled
* A list of all registered flights is viewable

### Acceptance Criteria

```gherkin
Given the air traffic controller is on the flight management dashboard
When they register a new flight by providing flight number, airline, origin/destination, scheduled time, and type
Then the flight is recorded in the system
And they can edit or cancel the flight
And they can view the list of all flights
```

**UML class diagram:** `experiments/project_9/class_diagram_65.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/flight/flight_router.py` | `AirTrafficController`, `FlightOperationsTeam` |
| `src/domain/flight/Flight.py` | `Flight`, `FlightStatus`, `FlightType`, `Permission`, `Resource`, `State` |
| `src/domain/runway/Runway.py` | `Resource` |
| `src/dto/flight/flight_dto.py` | `FlightRegistrationRequest`, `FlightUpdateRequest` |
| `src/repository/flight/flight_repository.py` | `FlightDataStore`, `FlightManagementDashboard`, `FlightRegistrationAPI` |
| `src/service/flight/flight_service.py` | `FlightService` |
| `src/service/runway/runway_service.py` | `Permission` |

---

### Task #66 — Slot Allocation with Gap

**As a** air traffic controller
**I need** the system to allocate 5-minute time slots for flights with a mandatory 3-minute gap between consecutive slots
**So that** ensure safe separation

### Details and Assumptions
* The system automatically assigns time slots to flights based on scheduling rules.
* Each flight receives a dedicated 5-minute slot.
* A mandatory 3-minute gap is enforced between the end of one slot and the start of the next slot.

### Acceptance Criteria

```gherkin
Given a flight schedule
When the system allocates time slots
Then each flight gets a 5-minute slot
And there is a 3-minute gap between the end of one slot and the start of the next
And slots are automatically assigned based on scheduling rules
```

**UML class diagram:** `experiments/project_9/class_diagram_66.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/flight/Flight.py` | `Flight`, `FlightStatus`, `Permission`, `Resource`, `State` |
| `src/domain/runway/Runway.py` | `Interface`, `Operation`, `Resource` |
| `src/domain/time_slot/TimeSlot.py` | `TimeSlot` |
| `src/service/runway/runway_service.py` | `Actor`, `Permission` |

---

### Task #67 — Arrival Priority Over Departures

**As a** air traffic controller
**I need** arrivals to be prioritized over departures during slot allocation
**So that** holding patterns are reduced and landing efficiency is improved

### Details and Assumptions
* This feature applies to a slot allocation system for an airport or airspace.
* Arriving flights are considered higher priority than departing flights when slot conflicts occur.
* Departure slots are adjusted after arrival slots are finalized.

### Acceptance Criteria

```gherkin
Given there is a slot conflict between an arriving flight and a departing flight
When the slot allocation algorithm runs
Then the arriving flight is assigned the conflicting slot
And the departing flight is assigned an alternative slot
```

```gherkin
Given a set of arrival and departure requests for a given time window
When the slot allocation algorithm processes the requests
Then all arrival slots are placed before any departure slots are adjusted
```

```gherkin
Given the slot allocation priority logic has been implemented
When a new conflict scenario is encountered
Then the prioritization rules are clearly documented and accessible
```

**UML class diagram:** `experiments/project_9/class_diagram_67.puml`

*(No generated files matched classes from this task's UML diagram)*

---

### Task #68 — Overlap and Gap Violation Detection

**As a** system monitor
**I need** the system to automatically detect overlapping assignments or violations of the 3-minute gap rule
**So that** scheduling conflicts can be flagged

### Details and Assumptions
* The system manages flight assignments and time slots.
* Overlapping assignments mean two flights occupy time windows that intersect.
* The 3-minute gap rule requires at least 3 minutes between the end of one slot and the start of the next.

### Acceptance Criteria

```gherkin
Given two flights occupy overlapping time windows
When the system is monitoring
Then alerts are triggered

Given the gap between two slots is less than 3 minutes
When the system is monitoring
Then alerts are triggered

Given a scheduling violation is detected
When the system is monitoring
Then a visual/notification indicator of the violation is shown
```

**UML class diagram:** `experiments/project_9/class_diagram_68.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/flight/Flight.py` | `Permission`, `Resource`, `State` |
| `src/domain/runway/Runway.py` | `Operation`, `Resource` |
| `src/domain/time_slot/TimeSlot.py` | `TimeSlot` |
| `src/service/runway/runway_service.py` | `Actor`, `Permission` |

---

### Task #69 — Runway Closure Handling

**As a** air traffic controller
**I need** to handle a runway closure by having the system automatically reassign affected flights to alternative runways (if available) or reschedule them
**So that** I can manage runway closures efficiently and minimize flight disruptions

### Details and Assumptions
* The system must identify all flights currently scheduled for the closed runway.
* If alternative runways are available, the system should suggest reassignments based on operational constraints (e.g., runway length, aircraft type).
* If no alternative runways are available, the system should queue the affected flights and reschedule them with updated times.
* The air traffic controller can review and approve or override the system's suggestions.

### Acceptance Criteria

```gherkin
Given a runway is marked as closed
When the system processes the closure
Then it automatically identifies all affected flights scheduled on that runway

Given affected flights are identified
When there is at least one alternative runway available
Then the system suggests reassigning those flights to the alternative runways

Given affected flights are identified
When no alternative runway is available
Then the system queues those flights and reschedules them with new times
```

**UML class diagram:** `experiments/project_9/class_diagram_69.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/flight/Flight.py` | `Flight`, `FlightStatus`, `Permission`, `Resource` |
| `src/domain/runway/Runway.py` | `AlternativeRunway`, `Channel`, `Interface`, `Operation`, `Resource`, `Runway`, `Slot` |
| `src/repository/runway/runway_repository.py` | `AirTrafficControlConsole`, `FlightSchedulingAPI`, `RunwayStatusDatabase` |
| `src/service/runway/runway_service.py` | `AirTrafficControl`, `FlightOperations`, `Passengers`, `Permission` |

---

### Task #70 — Emergency Priority Slot

**As a** air traffic controller
**I need** to declare an emergency for a flight and have the system assign an immediate priority slot overriding normal scheduling rules
**So that** the emergency flight can be prioritized and accommodated without delay

### Details and Assumptions
* The system currently uses normal scheduling rules for slot assignment
* Emergency flights require immediate priority over other scheduled flights
* Other flights' slots must be adjusted to accommodate the emergency

### Acceptance Criteria

```gherkin
Given I am viewing a flight in the system
When I select the option to mark the flight as an emergency
Then the system assigns an immediate priority slot to that flight

Given an emergency flight has been assigned a priority slot
When the system processes the slot assignment
Then other scheduled slots are automatically adjusted to accommodate the emergency flight
```

**UML class diagram:** `experiments/project_9/class_diagram_70.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/flight/flight_router.py` | `AirTrafficController` |
| `src/domain/flight/Flight.py` | `Flight`, `Permission`, `Resource`, `State` |
| `src/domain/runway/Runway.py` | `Channel`, `Operation`, `Resource`, `Slot` |
| `src/service/runway/runway_service.py` | `Actor`, `Permission` |

---

### Task #71 — Runway Slot Timetable Display

**As a** air traffic controller
**I need** view a runway slot timetable that shows all allocated slots with clear indicators for delays and emergencies
**So that** maintain situational awareness

### Details and Assumptions
* Timetable shows all allocated slots per runway
* Delayed flights are highlighted with delay duration
* Emergency flights are highlighted with a special marker
* Timetable can be filtered by runway and time

### Acceptance Criteria

```gherkin
Given the air traffic controller is viewing the runway slot timetable
When the timetable is loaded
Then the timetable displays all allocated slots per runway with delayed flights highlighted by delay duration and emergency flights marked with a special marker, and the timetable can be filtered by runway and time
```

**UML class diagram:** `experiments/project_9/class_diagram_71.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/flight/Flight.py` | `Permission`, `Resource`, `State` |
| `src/domain/runway/Runway.py` | `Interface`, `Operation`, `Resource` |
| `src/service/runway/runway_service.py` | `Actor`, `Permission` |

---
