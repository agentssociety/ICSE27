# Project 12 — Scaffold Reference

Auto-generated from the persisted package design, requirement artifacts, and UML diagrams.
Intended as a navigation aid for follow-up agents and developers.

---

## Statistics

| Item | Count |
|------|-------|
| Packages | 51 |
| Requirements linked | 8 |
| Tasks | 8 |
| Domain classes | 6 |

---

## Notes

- Generated files are implementation skeletons intended to be filled in by follow-up agents or developers.
- Existing files are preserved unless `overwrite_existing=True` is used.

---

## File Index

All generated files organised by package.

### `domain.card` · layer: `domain`

Path: `src/domain/card`
> Domain layer for the Card domain class

| File | Classes |
|------|---------|
| `Card.py` | `Actor`, `Permission`, `Resource`, `Credential`, `Digit`, `State`, `IfaceKind`, `Bool`, `Card`, `CardId`, `CardCreatedEvent`, `CardUpdatedEvent` |

### `dto.card` · layer: `dto`

Path: `src/dto/card`
> Dto layer for the Card domain class

| File | Classes |
|------|---------|
| `card_dto.py` | `CardCreateRequest`, `CardUpdateRequest`, `CardResponse` |

### `repository.card` · layer: `repository`

Path: `src/repository/card`
> Repository layer for the Card domain class

| File | Classes |
|------|---------|
| `card_repository.py` | `Interface`, `CardReader`, `PINVerificationService` |

### `orm.card` · layer: `orm`

Path: `src/orm/card`
> Orm layer for the Card domain class

| File | Classes |
|------|---------|
| `card_orm.py` | `CardORM` |

### `infra.card` · layer: `infra`

Path: `src/infra/card`
> Infra layer for the Card domain class

| File | Classes |
|------|---------|
| `card_repo_impl.py` | `SQLAlchemyCardRepository` |

### `service.card` · layer: `service`

Path: `src/service/card`
> Service layer for the Card domain class

| File | Classes |
|------|---------|
| `card_service.py` | `CardService`, `CardServiceImpl` |

### `api.card` · layer: `api`

Path: `src/api/card`
> Api layer for the Card domain class

| File | Classes |
|------|---------|
| `card_router.py` | `CardRouter` |

### `tests.unit.card` · layer: `tests`

Path: `tests/unit/card`
> Unit tests for Card across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_card_domain.py` | — |
| `test_card_service.py` | — |
| `test_card_api.py` | — |

### `domain.pin` · layer: `domain`

Path: `src/domain/pin`
> Domain layer for the Pin domain class

| File | Classes |
|------|---------|
| `Pin.py` | `Actor`, `Permission`, `Resource`, `Credential`, `Pin`, `Digit`, `State`, `IfaceKind`, `Bool`, `PinId`, `PinCreatedEvent`, `PinUpdatedEvent` |

### `dto.pin` · layer: `dto`

Path: `src/dto/pin`
> Dto layer for the Pin domain class

| File | Classes |
|------|---------|
| `pin_dto.py` | `PinCreateRequest`, `PinUpdateRequest`, `PinResponse` |

### `repository.pin` · layer: `repository`

Path: `src/repository/pin`
> Repository layer for the Pin domain class

| File | Classes |
|------|---------|
| `pin_repository.py` | `Interface`, `CardReader`, `PINVerificationService` |

### `orm.pin` · layer: `orm`

Path: `src/orm/pin`
> Orm layer for the Pin domain class

| File | Classes |
|------|---------|
| `pin_orm.py` | `PinORM` |

### `infra.pin` · layer: `infra`

Path: `src/infra/pin`
> Infra layer for the Pin domain class

| File | Classes |
|------|---------|
| `pin_repo_impl.py` | `SQLAlchemyPinRepository` |

### `service.pin` · layer: `service`

Path: `src/service/pin`
> Service layer for the Pin domain class

| File | Classes |
|------|---------|
| `pin_service.py` | `PinService`, `PinServiceImpl` |

### `api.pin` · layer: `api`

Path: `src/api/pin`
> Api layer for the Pin domain class

| File | Classes |
|------|---------|
| `pin_router.py` | `PinRouter` |

### `tests.unit.pin` · layer: `tests`

Path: `tests/unit/pin`
> Unit tests for Pin across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_pin_domain.py` | — |
| `test_pin_service.py` | — |
| `test_pin_api.py` | — |

### `domain.user` · layer: `domain`

Path: `src/domain/user`
> Domain layer for the User domain class

| File | Classes |
|------|---------|
| `User.py` | `Actor`, `Permission`, `Resource`, `Credential`, `Digit`, `State`, `IfaceKind`, `Bool`, `User`, `UserId`, `UserCreatedEvent`, `UserUpdatedEvent` |

### `dto.user` · layer: `dto`

Path: `src/dto/user`
> Dto layer for the User domain class

| File | Classes |
|------|---------|
| `user_dto.py` | `UserCreateRequest`, `UserUpdateRequest`, `UserResponse` |

### `repository.user` · layer: `repository`

Path: `src/repository/user`
> Repository layer for the User domain class

| File | Classes |
|------|---------|
| `user_repository.py` | `Interface`, `CardReader`, `PINVerificationService` |

### `orm.user` · layer: `orm`

Path: `src/orm/user`
> Orm layer for the User domain class

| File | Classes |
|------|---------|
| `user_orm.py` | `UserORM` |

### `infra.user` · layer: `infra`

Path: `src/infra/user`
> Infra layer for the User domain class

| File | Classes |
|------|---------|
| `user_repo_impl.py` | `SQLAlchemyUserRepository` |

### `service.user` · layer: `service`

Path: `src/service/user`
> Service layer for the User domain class

| File | Classes |
|------|---------|
| `user_service.py` | `UserService`, `UserServiceImpl` |

### `api.user` · layer: `api`

Path: `src/api/user`
> Api layer for the User domain class

| File | Classes |
|------|---------|
| `user_router.py` | `UserRouter` |

### `tests.unit.user` · layer: `tests`

Path: `tests/unit/user`
> Unit tests for User across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_user_domain.py` | — |
| `test_user_service.py` | — |
| `test_user_api.py` | — |

### `domain.audit_log_entry` · layer: `domain`

Path: `src/domain/audit_log_entry`
> Domain layer for the AuditLogEntry domain class

| File | Classes |
|------|---------|
| `AuditLogEntry.py` | `AuditLogEntry`, `AuditLogEntryId`, `AuditLogEntryCreatedEvent`, `AuditLogEntryUpdatedEvent` |

### `dto.audit_log_entry` · layer: `dto`

Path: `src/dto/audit_log_entry`
> Dto layer for the AuditLogEntry domain class

| File | Classes |
|------|---------|
| `audit_log_entry_dto.py` | `AuditLogEntryCreateRequest`, `AuditLogEntryUpdateRequest`, `AuditLogEntryResponse` |

### `repository.audit_log_entry` · layer: `repository`

Path: `src/repository/audit_log_entry`
> Repository layer for the AuditLogEntry domain class

| File | Classes |
|------|---------|
| `audit_log_entry_repository.py` | `AuditLogEntryRepository` |

### `orm.audit_log_entry` · layer: `orm`

Path: `src/orm/audit_log_entry`
> Orm layer for the AuditLogEntry domain class

| File | Classes |
|------|---------|
| `audit_log_entry_orm.py` | `AuditLogEntryORM` |

### `infra.audit_log_entry` · layer: `infra`

Path: `src/infra/audit_log_entry`
> Infra layer for the AuditLogEntry domain class

| File | Classes |
|------|---------|
| `audit_log_entry_repo_impl.py` | `SQLAlchemyAuditLogEntryRepository` |

### `service.audit_log_entry` · layer: `service`

Path: `src/service/audit_log_entry`
> Service layer for the AuditLogEntry domain class

| File | Classes |
|------|---------|
| `audit_log_entry_service.py` | `AuditLogEntryService`, `AuditLogEntryServiceImpl` |

### `api.audit_log_entry` · layer: `api`

Path: `src/api/audit_log_entry`
> Api layer for the AuditLogEntry domain class

| File | Classes |
|------|---------|
| `audit_log_entry_router.py` | `AuditLogEntryRouter` |

### `tests.unit.audit_log_entry` · layer: `tests`

Path: `tests/unit/audit_log_entry`
> Unit tests for AuditLogEntry across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_audit_log_entry_domain.py` | — |
| `test_audit_log_entry_service.py` | — |
| `test_audit_log_entry_api.py` | — |

### `domain.transaction` · layer: `domain`

Path: `src/domain/transaction`
> Domain layer for the Transaction domain class

| File | Classes |
|------|---------|
| `Transaction.py` | `Transaction`, `FlaggedTransaction`, `FraudAnalyst`, `System`, `Permission`, `State`, `TransactionStatus`, `FlaggedTransactionStatus`, `Actor`, `SystemAdministrator`, `TransactionId`, `TransactionCreatedEvent`, `TransactionUpdatedEvent` |

### `dto.transaction` · layer: `dto`

Path: `src/dto/transaction`
> Dto layer for the Transaction domain class

| File | Classes |
|------|---------|
| `transaction_dto.py` | `TransactionCreateRequest`, `TransactionUpdateRequest`, `TransactionResponse` |

### `repository.transaction` · layer: `repository`

Path: `src/repository/transaction`
> Repository layer for the Transaction domain class

| File | Classes |
|------|---------|
| `transaction_repository.py` | `FlaggedTransactionsReviewPage`, `TransactionsDatabase`, `AuthenticationAuthorizationService` |

### `orm.transaction` · layer: `orm`

Path: `src/orm/transaction`
> Orm layer for the Transaction domain class

| File | Classes |
|------|---------|
| `transaction_orm.py` | `TransactionORM` |

### `infra.transaction` · layer: `infra`

Path: `src/infra/transaction`
> Infra layer for the Transaction domain class

| File | Classes |
|------|---------|
| `transaction_repo_impl.py` | `SQLAlchemyTransactionRepository` |

### `service.transaction` · layer: `service`

Path: `src/service/transaction`
> Service layer for the Transaction domain class

| File | Classes |
|------|---------|
| `transaction_service.py` | `TransactionService`, `TransactionServiceImpl` |

### `api.transaction` · layer: `api`

Path: `src/api/transaction`
> Api layer for the Transaction domain class

| File | Classes |
|------|---------|
| `transaction_router.py` | `TransactionRouter` |

### `tests.unit.transaction` · layer: `tests`

Path: `tests/unit/transaction`
> Unit tests for Transaction across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_transaction_domain.py` | — |
| `test_transaction_service.py` | — |
| `test_transaction_api.py` | — |

### `domain.account` · layer: `domain`

Path: `src/domain/account`
> Domain layer for the Account domain class

| File | Classes |
|------|---------|
| `Account.py` | `Account`, `Actor`, `Resource`, `Operation`, `LockStatus`, `PermissionType`, `Permission`, `FailedAttempt`, `State`, `StateValue`, `AccountStatus`, `UserAccount`, `Admin`, `SecurityTeam`, `AccountId`, `AccountCreatedEvent`, `AccountUpdatedEvent` |

### `dto.account` · layer: `dto`

Path: `src/dto/account`
> Dto layer for the Account domain class

| File | Classes |
|------|---------|
| `account_dto.py` | `LoginRequestDTO`, `LoginResponseDTO`, `UnlockRequestDTO`, `UnlockResponseDTO`, `AuthorizationRequest`, `AuthorizationResponse`, `AccountData` |

### `repository.account` · layer: `repository`

Path: `src/repository/account`
> Repository layer for the Account domain class

| File | Classes |
|------|---------|
| `account_repository.py` | `Interface`, `Account_Database`, `Payment_Processing_System`, `LockUnlockAPI`, `UserManagementDatabase`, `UserManagementPage` |

### `orm.account` · layer: `orm`

Path: `src/orm/account`
> Orm layer for the Account domain class

| File | Classes |
|------|---------|
| `account_orm.py` | `AccountORM` |

### `infra.account` · layer: `infra`

Path: `src/infra/account`
> Infra layer for the Account domain class

| File | Classes |
|------|---------|
| `account_repo_impl.py` | `SQLAlchemyAccountRepository` |

### `service.account` · layer: `service`

Path: `src/service/account`
> Service layer for the Account domain class

| File | Classes |
|------|---------|
| `account_service.py` | `Operation`, `LockUnlockService` |

### `api.account` · layer: `api`

Path: `src/api/account`
> Api layer for the Account domain class

| File | Classes |
|------|---------|
| `account_router.py` | `LoginController`, `AdminController`, `AccountController` |

### `tests.unit.account` · layer: `tests`

Path: `tests/unit/account`
> Unit tests for Account across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_account_domain.py` | — |
| `test_account_service.py` | — |
| `test_account_api.py` | — |

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
| `test_user_flow.py` | — |
| `test_card_flow.py` | — |
| `test_pin_flow.py` | — |
| `test_audit_log_entry_flow.py` | — |
| `test_transaction_flow.py` | — |
| `test_account_flow.py` | — |
| `test_api_contracts.py` | — |
| `conftest.py` | — |

---

## Task Index

For each task: full description, files whose classes appear in the task's UML diagram,
and paths to the linked requirement specification and UML diagrams.

### Task #88 — Card and PIN Authentication

**As a** user
**I need** card and PIN authentication
**So that** I can securely access the system

### Details and Assumptions
* The system will require both a physical card and a PIN for authentication.
* This is a security feature for user access control.

### Acceptance Criteria

```gherkin
Given a registered user with a valid card and known PIN
When the user inserts the card and enters their PIN
Then the system authenticates the user and grants access
```

**UML class diagram:** `experiments/project_12/class_diagram_88.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/account/Account.py` | `Actor`, `Permission`, `Resource` |
| `src/domain/card/Card.py` | `Actor`, `Bool`, `Credential`, `Digit`, `IfaceKind`, `Permission`, `Resource` |
| `src/domain/pin/Pin.py` | `Actor`, `Bool`, `Credential`, `Digit`, `IfaceKind`, `Permission`, `Pin`, `Resource` |
| `src/domain/transaction/Transaction.py` | `Actor`, `Permission` |
| `src/domain/user/User.py` | `Actor`, `Bool`, `Credential`, `Digit`, `IfaceKind`, `Permission`, `Resource` |
| `src/repository/account/account_repository.py` | `Interface` |
| `src/repository/card/card_repository.py` | `CardReader`, `Interface`, `PINVerificationService` |
| `src/repository/pin/pin_repository.py` | `CardReader`, `Interface`, `PINVerificationService` |
| `src/repository/user/user_repository.py` | `CardReader`, `Interface`, `PINVerificationService` |

---

### Task #89 — Account Lockout After 3 Failed Attempts

**As a** user
**I need** my account to be locked after three consecutive failed PIN attempts
**So that** brute force attacks are prevented

### Details and Assumptions
* The lock applies after three failed attempts in a row.
* The account remains locked until manually unlocked by an administrator or after a defined cooldown period (not specified here).

### Acceptance Criteria

```gherkin
Given the user has entered an incorrect PIN three times consecutively
When the user attempts to enter a PIN a fourth time
Then the account is locked and the user is notified of the lock
```

**UML class diagram:** `experiments/project_12/class_diagram_89.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/account/account_router.py` | `AdminController`, `LoginController` |
| `src/domain/account/Account.py` | `Account`, `Actor`, `FailedAttempt`, `LockStatus`, `Operation`, `Permission`, `PermissionType`, `Resource`, `State`, `StateValue` |
| `src/domain/card/Card.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/pin/Pin.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/transaction/Transaction.py` | `Actor`, `Permission`, `State` |
| `src/domain/user/User.py` | `Actor`, `Permission`, `Resource`, `State`, `User` |
| `src/dto/account/account_dto.py` | `LoginRequestDTO`, `LoginResponseDTO`, `UnlockRequestDTO`, `UnlockResponseDTO` |
| `src/service/account/account_service.py` | `Operation` |

---

### Task #90 — Balance and Daily Limit Enforcement

**As a** account holder
**I need** the system to enforce balance checks and daily transaction limits
**So that** I cannot overdraw my account or make excessive transactions

### Details and Assumptions
* The system will check the account balance before authorizing any transaction.
* A daily transaction limit (number or total amount) is defined per account.
* Transactions that would exceed the balance or daily limit are rejected.
* The user is notified if a transaction is blocked.

### Acceptance Criteria

```gherkin
Given an account with a balance of $100 and a daily transaction limit of $200
When a transaction of $150 is attempted
Then the transaction is authorized

Given an account with a balance of $100 and a daily transaction limit of $200
When a transaction of $120 is attempted
Then the transaction is rejected due to insufficient funds

Given an account that has already used $180 of its $200 daily limit
When a transaction of $30 is attempted
Then the transaction is rejected due to exceeding the daily limit

Given an account that has already used $180 of its $200 daily limit
When a transaction of $20 is attempted
Then the transaction is authorized
```

**UML class diagram:** `experiments/project_12/class_diagram_90.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/account/Account.py` | `Account`, `Actor`, `Operation`, `Permission`, `Resource`, `State` |
| `src/domain/card/Card.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/pin/Pin.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/transaction/Transaction.py` | `Actor`, `Permission`, `State`, `Transaction` |
| `src/domain/user/User.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/dto/account/account_dto.py` | `AccountData`, `AuthorizationRequest`, `AuthorizationResponse` |
| `src/repository/account/account_repository.py` | `Account_Database`, `Interface`, `Payment_Processing_System` |
| `src/repository/card/card_repository.py` | `Interface` |
| `src/repository/pin/pin_repository.py` | `Interface` |
| `src/repository/user/user_repository.py` | `Interface` |
| `src/service/account/account_service.py` | `Operation` |

---

### Task #91 — Atomic Transaction with Rollback

**As a** developer  
**I need** to implement atomic transactions that ensure all-or-nothing execution with rollback capability on failure  
**So that** data remains consistent even if an operation fails  

### Details and Assumptions
* The feature must support grouping multiple operations into a single transaction.
* If any operation within the transaction fails, all previous operations must be rolled back.
* The transaction should be either fully committed or fully rolled back with no partial state changes.
* The implementation should handle errors such as system crashes, network failures, or invalid data.

### Acceptance Criteria

```gherkin
Given a transaction with multiple operations
When all operations succeed
Then the transaction is committed
And all changes are persisted

Given a transaction with multiple operations
When one or more operations fail
Then the transaction is rolled back
And no changes from the transaction are persisted
```

**UML class diagram:** `experiments/project_12/class_diagram_91.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/account/Account.py` | `Actor`, `Operation`, `Permission`, `Resource`, `State` |
| `src/domain/card/Card.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/pin/Pin.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/transaction/Transaction.py` | `Actor`, `Permission`, `State`, `Transaction` |
| `src/domain/user/User.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/repository/account/account_repository.py` | `Interface` |
| `src/repository/card/card_repository.py` | `Interface` |
| `src/repository/pin/pin_repository.py` | `Interface` |
| `src/repository/user/user_repository.py` | `Interface` |
| `src/service/account/account_service.py` | `Operation` |

---

### Task #92 — Suspicious Pattern Detection and Flagging

**As a** fraud analyst
**I need** the system to detect suspicious transaction patterns such as multiple rapid withdrawals
**So that** I can flag them for review and prevent potential fraud

### Details and Assumptions
* The system monitors transaction frequency and speed
* Multiple rapid withdrawals are considered a suspicious pattern
* Flagged transactions are queued for manual review

### Acceptance Criteria

```gherkin
Given a user initiates multiple rapid withdrawals
When the system detects this pattern
Then the transactions are flagged for review
```

**UML class diagram:** `experiments/project_12/class_diagram_92.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/account/Account.py` | `Permission`, `State` |
| `src/domain/card/Card.py` | `Permission`, `State` |
| `src/domain/pin/Pin.py` | `Permission`, `State` |
| `src/domain/transaction/Transaction.py` | `FlaggedTransaction`, `FlaggedTransactionStatus`, `FraudAnalyst`, `Permission`, `State`, `System`, `Transaction`, `TransactionStatus` |
| `src/domain/user/User.py` | `Permission`, `State`, `User` |

---

### Task #93 — Admin Review of Flagged Transactions

**As a** system administrator
**I need** an interface to review and act on flagged transactions
**So that** I can investigate suspicious activity and take appropriate actions to maintain system integrity

### Details and Assumptions
* Flagged transactions have been identified by fraud detection/system rules
* Actions may include approving, denying, or further investigating transactions
* The interface provides filtering and sorting capabilities

### Acceptance Criteria

```gherkin
Given an admin user is logged in and on the flagged transactions review page
When the user views the list
Then all transactions flagged by the system are displayed with relevant details

Given a flagged transaction is displayed
When the admin selects an action (approve/deny/investigate)
Then the system updates the transaction status and removes it from the pending review list
```

**UML class diagram:** `experiments/project_12/class_diagram_93.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/account/Account.py` | `Permission` |
| `src/domain/card/Card.py` | `Permission` |
| `src/domain/pin/Pin.py` | `Permission` |
| `src/domain/transaction/Transaction.py` | `FlaggedTransaction`, `Permission`, `SystemAdministrator`, `TransactionStatus` |
| `src/domain/user/User.py` | `Permission`, `User` |
| `src/repository/transaction/transaction_repository.py` | `AuthenticationAuthorizationService`, `FlaggedTransactionsReviewPage` |

---

### Task #94 — Admin Lock/Unlock Accounts

**As a** admin
**I need** to manually lock or unlock user accounts
**So that** I can control user access and security

### Details and Assumptions
* There is an existing user management interface for admins.
* Locking an account prevents the user from logging in or performing actions.
* Unlocking restores full access.
* Admin has proper authentication and authorization.

### Acceptance Criteria

```gherkin
Given I am an authenticated admin on the user management page
When I select a user account and choose to lock it
Then the account status changes to "locked" and the user cannot log in

Given I am an authenticated admin on the user management page
When I select a locked user account and choose to unlock it
Then the account status changes to "active" and the user can log in again
```

**UML class diagram:** `experiments/project_12/class_diagram_94.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/account/account_router.py` | `AccountController` |
| `src/domain/account/Account.py` | `AccountStatus`, `Admin`, `Permission`, `SecurityTeam`, `UserAccount` |
| `src/domain/card/Card.py` | `Permission` |
| `src/domain/pin/Pin.py` | `Permission` |
| `src/domain/transaction/Transaction.py` | `Permission` |
| `src/domain/user/User.py` | `Permission` |
| `src/repository/account/account_repository.py` | `LockUnlockAPI`, `UserManagementDatabase`, `UserManagementPage` |
| `src/service/account/account_service.py` | `LockUnlockService` |

---

### Task #95 — Audit Log with Timestamps

**As a** security administrator
**I need** to maintain an audit log that records all security-relevant events with precise timestamps
**So that** I can monitor, investigate, and ensure compliance with security policies

### Details and Assumptions
* The audit log must record events such as login attempts, access to sensitive data, permission changes, and failed actions.
* Each log entry must include the event type, timestamp (with millisecond precision), user ID, source IP, and outcome.
* The log must be append-only and tamper-proof to guarantee integrity.
* Logs should be searchable and exportable for analysis.

### Acceptance Criteria

```gherkin
Given a security-relevant event occurs  
When the system processes the event  
Then the event is recorded in the audit log  
And the log entry includes a precise timestamp (YYYY-MM-DDTHH:mm:ss.sssZ)  
And the event type, user ID, and outcome are captured  
And the log cannot be modified or deleted after creation
```

**UML class diagram:** `experiments/project_12/class_diagram_95.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/account/Account.py` | `Actor`, `Operation`, `Permission`, `Resource`, `State` |
| `src/domain/audit_log_entry/AuditLogEntry.py` | `AuditLogEntry` |
| `src/domain/card/Card.py` | `Actor`, `IfaceKind`, `Permission`, `Resource`, `State` |
| `src/domain/pin/Pin.py` | `Actor`, `IfaceKind`, `Permission`, `Resource`, `State` |
| `src/domain/transaction/Transaction.py` | `Actor`, `Permission`, `State` |
| `src/domain/user/User.py` | `Actor`, `IfaceKind`, `Permission`, `Resource`, `State` |
| `src/repository/account/account_repository.py` | `Interface` |
| `src/repository/card/card_repository.py` | `Interface` |
| `src/repository/pin/pin_repository.py` | `Interface` |
| `src/repository/user/user_repository.py` | `Interface` |
| `src/service/account/account_service.py` | `Operation` |

---
