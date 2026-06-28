# Project 11 — Scaffold Reference

Auto-generated from the persisted package design, requirement artifacts, and UML diagrams.
Intended as a navigation aid for follow-up agents and developers.

---

## Statistics

| Item | Count |
|------|-------|
| Packages | 61 |
| Requirements linked | 8 |
| Tasks | 8 |
| Domain classes | 7 |

---

## Notes

- Generated files are implementation skeletons intended to be filled in by follow-up agents or developers.
- Existing files are preserved unless `overwrite_existing=True` is used.

---

## File Index

All generated files organised by package.

### `domain.account` · layer: `domain`

Path: `src/domain/account`
> Domain layer for the Account domain class

| File | Classes |
|------|---------|
| `Account.py` | `Actor`, `Account`, `AccountState`, `Permission`, `AccountId`, `AccountCreatedEvent`, `AccountUpdatedEvent` |

### `dto.account` · layer: `dto`

Path: `src/dto/account`
> Dto layer for the Account domain class

| File | Classes |
|------|---------|
| `account_dto.py` | `AuthenticationRequest`, `AuthenticationResponse` |

### `repository.account` · layer: `repository`

Path: `src/repository/account`
> Repository layer for the Account domain class

| File | Classes |
|------|---------|
| `account_repository.py` | `AuthenticationAPI`, `UserAuthenticationDatabase` |

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
| `account_service.py` | `AuthenticationFlow` |

### `api.account` · layer: `api`

Path: `src/api/account`
> Api layer for the Account domain class

| File | Classes |
|------|---------|
| `account_router.py` | `AuthenticationController` |

### `tests.unit.account` · layer: `tests`

Path: `tests/unit/account`
> Unit tests for Account across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_account_domain.py` | — |
| `test_account_service.py` | — |
| `test_account_api.py` | — |

### `domain.card` · layer: `domain`

Path: `src/domain/card`
> Domain layer for the Card domain class

| File | Classes |
|------|---------|
| `Card.py` | `Actor`, `Card`, `AccountState`, `Permission`, `CardId`, `CardCreatedEvent`, `CardUpdatedEvent` |

### `dto.card` · layer: `dto`

Path: `src/dto/card`
> Dto layer for the Card domain class

| File | Classes |
|------|---------|
| `card_dto.py` | `AuthenticationRequest`, `AuthenticationResponse` |

### `repository.card` · layer: `repository`

Path: `src/repository/card`
> Repository layer for the Card domain class

| File | Classes |
|------|---------|
| `card_repository.py` | `AuthenticationAPI`, `UserAuthenticationDatabase` |

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
| `card_service.py` | `AuthenticationFlow` |

### `api.card` · layer: `api`

Path: `src/api/card`
> Api layer for the Card domain class

| File | Classes |
|------|---------|
| `card_router.py` | `AuthenticationController` |

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
> Domain layer for the PIN domain class

| File | Classes |
|------|---------|
| `PIN.py` | `PIN`, `PINId`, `PINCreatedEvent`, `PINUpdatedEvent` |

### `dto.pin` · layer: `dto`

Path: `src/dto/pin`
> Dto layer for the PIN domain class

| File | Classes |
|------|---------|
| `pin_dto.py` | `PINCreateRequest`, `PINUpdateRequest`, `PINResponse` |

### `repository.pin` · layer: `repository`

Path: `src/repository/pin`
> Repository layer for the PIN domain class

| File | Classes |
|------|---------|
| `pin_repository.py` | `PINRepository` |

### `orm.pin` · layer: `orm`

Path: `src/orm/pin`
> Orm layer for the PIN domain class

| File | Classes |
|------|---------|
| `pin_orm.py` | `PINORM` |

### `infra.pin` · layer: `infra`

Path: `src/infra/pin`
> Infra layer for the PIN domain class

| File | Classes |
|------|---------|
| `pin_repo_impl.py` | `SQLAlchemyPINRepository` |

### `service.pin` · layer: `service`

Path: `src/service/pin`
> Service layer for the PIN domain class

| File | Classes |
|------|---------|
| `pin_service.py` | `PINService`, `PINServiceImpl` |

### `api.pin` · layer: `api`

Path: `src/api/pin`
> Api layer for the PIN domain class

| File | Classes |
|------|---------|
| `pin_router.py` | `PINRouter` |

### `tests.unit.pin` · layer: `tests`

Path: `tests/unit/pin`
> Unit tests for PIN across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_pin_domain.py` | — |
| `test_pin_service.py` | — |
| `test_pin_api.py` | — |

### `domain.transaction` · layer: `domain`

Path: `src/domain/transaction`
> Domain layer for the Transaction domain class

| File | Classes |
|------|---------|
| `Transaction.py` | `Transaction`, `WithdrawalRecord`, `Permission`, `State`, `FailureReason`, `Role`, `WithdrawalStatus`, `Money`, `TransactionId`, `TransactionCreatedEvent`, `TransactionUpdatedEvent` |

### `dto.transaction` · layer: `dto`

Path: `src/dto/transaction`
> Dto layer for the Transaction domain class

| File | Classes |
|------|---------|
| `transaction_dto.py` | `WithdrawalRequestDTO`, `WithdrawalResponseDTO`, `ErrorResponseDTO` |

### `repository.transaction` · layer: `repository`

Path: `src/repository/transaction`
> Repository layer for the Transaction domain class

| File | Classes |
|------|---------|
| `transaction_repository.py` | `TransactionRepository` |

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

### `domain.account_flag` · layer: `domain`

Path: `src/domain/account_flag`
> Domain layer for the AccountFlag domain class

| File | Classes |
|------|---------|
| `AccountFlag.py` | `Permission`, `Bool`, `IfaceKind`, `Actor`, `Resource`, `Interface`, `State`, `REQ_FRAUD_01`, `AuditEntry`, `AccountFlag`, `AccountFlagId`, `AccountFlagCreatedEvent`, `AccountFlagUpdatedEvent` |

### `dto.account_flag` · layer: `dto`

Path: `src/dto/account_flag`
> Dto layer for the AccountFlag domain class

| File | Classes |
|------|---------|
| `account_flag_dto.py` | `AccountFlagCreateRequest`, `AccountFlagUpdateRequest`, `AccountFlagResponse` |

### `repository.account_flag` · layer: `repository`

Path: `src/repository/account_flag`
> Repository layer for the AccountFlag domain class

| File | Classes |
|------|---------|
| `account_flag_repository.py` | `AccountFlagRepository` |

### `orm.account_flag` · layer: `orm`

Path: `src/orm/account_flag`
> Orm layer for the AccountFlag domain class

| File | Classes |
|------|---------|
| `account_flag_orm.py` | `AccountFlagORM` |

### `infra.account_flag` · layer: `infra`

Path: `src/infra/account_flag`
> Infra layer for the AccountFlag domain class

| File | Classes |
|------|---------|
| `account_flag_repo_impl.py` | `SQLAlchemyAccountFlagRepository` |

### `service.account_flag` · layer: `service`

Path: `src/service/account_flag`
> Service layer for the AccountFlag domain class

| File | Classes |
|------|---------|
| `account_flag_service.py` | `AccountFlagService`, `AccountFlagServiceImpl` |

### `api.account_flag` · layer: `api`

Path: `src/api/account_flag`
> Api layer for the AccountFlag domain class

| File | Classes |
|------|---------|
| `account_flag_router.py` | `AccountFlagRouter` |

### `tests.unit.account_flag` · layer: `tests`

Path: `tests/unit/account_flag`
> Unit tests for AccountFlag across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_account_flag_domain.py` | — |
| `test_account_flag_service.py` | — |
| `test_account_flag_api.py` | — |

### `domain.user` · layer: `domain`

Path: `src/domain/user`
> Domain layer for the User domain class

| File | Classes |
|------|---------|
| `User.py` | `Actor`, `User`, `AccountState`, `Permission`, `UserId`, `UserCreatedEvent`, `UserUpdatedEvent` |

### `dto.user` · layer: `dto`

Path: `src/dto/user`
> Dto layer for the User domain class

| File | Classes |
|------|---------|
| `user_dto.py` | `AuthenticationRequest`, `AuthenticationResponse` |

### `repository.user` · layer: `repository`

Path: `src/repository/user`
> Repository layer for the User domain class

| File | Classes |
|------|---------|
| `user_repository.py` | `AuthenticationAPI`, `UserAuthenticationDatabase` |

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
| `user_service.py` | `AuthenticationFlow` |

### `api.user` · layer: `api`

Path: `src/api/user`
> Api layer for the User domain class

| File | Classes |
|------|---------|
| `user_router.py` | `AuthenticationController` |

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

### `shared.utilities` · layer: `infra`

Path: `src/infra/utilities`
> Cross-cutting concerns like hashing (PIN), date manipulation, and retry logic are needed across services and currently missing.

*(no files specified)*

### `config.limits_and_thresholds` · layer: `config`

Path: `src/config/limits_and_thresholds`
> Configuration for lockout attempts, daily withdrawal limits, suspicious pattern thresholds (e.g., rapid withdrawals, unusual amounts) is required by multiple services but not explicitly captured.

*(no files specified)*

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
| `test_account_flow.py` | — |
| `test_card_flow.py` | — |
| `test_pin_flow.py` | — |
| `test_transaction_flow.py` | — |
| `test_audit_log_entry_flow.py` | — |
| `test_account_flag_flow.py` | — |
| `test_api_contracts.py` | — |
| `conftest.py` | — |

---

## Task Index

For each task: full description, files whose classes appear in the task's UML diagram,
and paths to the linked requirement specification and UML diagrams.

### Task #79 — Card + PIN Authentication with Lockout

**As a** user
**I need** to authenticate using my card and PIN
**So that** my account is secure

### Details and Assumptions
* Authentication is card-and-PIN based.
* Account will be automatically locked after multiple failed attempts.

### Acceptance Criteria

```gherkin
Given I have a valid card and PIN
When I authenticate using my card and PIN
Then I am granted access to my account

Given I have an invalid card or PIN
When I attempt to authenticate multiple times
Then my account is automatically locked after a specified number of failed attempts
```

**UML class diagram:** `experiments/project_11/class_diagram_79.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/account/account_router.py` | `AuthenticationController` |
| `src/api/card/card_router.py` | `AuthenticationController` |
| `src/api/user/user_router.py` | `AuthenticationController` |
| `src/domain/account/Account.py` | `Account`, `AccountState`, `Permission` |
| `src/domain/account_flag/AccountFlag.py` | `Permission` |
| `src/domain/card/Card.py` | `AccountState`, `Card`, `Permission` |
| `src/domain/pin/PIN.py` | `PIN` |
| `src/domain/transaction/Transaction.py` | `Permission` |
| `src/domain/user/User.py` | `AccountState`, `Permission`, `User` |
| `src/dto/account/account_dto.py` | `AuthenticationRequest`, `AuthenticationResponse` |
| `src/dto/card/card_dto.py` | `AuthenticationRequest`, `AuthenticationResponse` |
| `src/dto/user/user_dto.py` | `AuthenticationRequest`, `AuthenticationResponse` |
| `src/repository/account/account_repository.py` | `AuthenticationAPI` |
| `src/repository/card/card_repository.py` | `AuthenticationAPI` |
| `src/repository/user/user_repository.py` | `AuthenticationAPI` |
| `src/service/account/account_service.py` | `AuthenticationFlow` |
| `src/service/card/card_service.py` | `AuthenticationFlow` |
| `src/service/user/user_service.py` | `AuthenticationFlow` |

---

### Task #80 — Balance and Daily Limit Enforcement

**As a** user
**I need** my transactions to respect the available balance and daily withdrawal limits
**So that** overdraw or limit exceedance is prevented

### Details and Assumptions
* The system checks the current available balance before processing any transaction.
* The system tracks daily withdrawal totals per user.
* Transactions that exceed the balance or daily limit are denied with an appropriate message.

### Acceptance Criteria

```gherkin
Given a user with an available balance and a daily withdrawal limit
When the user initiates a transaction
Then the system validates that the transaction amount does not exceed the available balance
And the system validates that the cumulative daily withdrawals including this transaction do not exceed the daily limit
And if either check fails, the transaction is denied
```

**UML class diagram:** `experiments/project_11/class_diagram_80.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/account/Account.py` | `Account`, `Permission` |
| `src/domain/account_flag/AccountFlag.py` | `Permission`, `State` |
| `src/domain/card/Card.py` | `Permission` |
| `src/domain/transaction/Transaction.py` | `Permission`, `State`, `Transaction` |
| `src/domain/user/User.py` | `Permission`, `User` |

---

### Task #82 — Atomic Withdrawal with Rollback

**As a** user
**I need** withdrawal operations to be atomic
**So that** in case of failure (e.g., network outage, system crash) the transaction is fully rolled back to maintain consistency

### Details and Assumptions
* The system must support atomic transactions for withdrawal operations.
* Atomicity ensures that if any part of the withdrawal fails, the entire operation is rolled back.
* The user's account balance should never be left in an inconsistent state.

### Acceptance Criteria

```gherkin
Given a user has a balance of $100
When the user initiates a withdrawal of $50
And a network failure occurs during the transaction
Then the user's balance should remain $100
And the withdrawal should not be recorded
```

**UML class diagram:** `experiments/project_11/class_diagram_82.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/account/Account.py` | `Account`, `Permission` |
| `src/domain/account_flag/AccountFlag.py` | `Permission`, `State` |
| `src/domain/card/Card.py` | `Permission` |
| `src/domain/transaction/Transaction.py` | `FailureReason`, `Money`, `Permission`, `Role`, `State`, `Transaction`, `TransactionId`, `WithdrawalRecord`, `WithdrawalStatus` |
| `src/domain/user/User.py` | `Permission`, `User` |
| `src/dto/transaction/transaction_dto.py` | `ErrorResponseDTO`, `WithdrawalRequestDTO`, `WithdrawalResponseDTO` |

---

### Task #83 — Suspicious Pattern Detection and Flagging

**As a** system
**I need** detect unusual withdrawal patterns (e.g., rapid consecutive withdrawals, unusual amounts) and flag the account for review
**So that** potential fraud or errors are identified quickly

### Details and Assumptions
* The system monitors all withdrawal transactions.
* Unusual patterns include rapid consecutive withdrawals (e.g., more than 3 within 5 minutes) or amounts significantly outside the user's historical average.
* Flagging involves setting an internal status on the account for manual review.

### Acceptance Criteria

```gherkin
Given the system is monitoring withdrawal transactions
When a user performs rapid consecutive withdrawals (e.g., 4 withdrawals within 5 minutes)
Then the system flags the account for review

Given the system is monitoring withdrawal transactions
When a user performs a withdrawal of an unusual amount (e.g., 10x the average)
Then the system flags the account for review
```

**UML class diagram:** `experiments/project_11/class_diagram_83.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/account/Account.py` | `Actor`, `Permission` |
| `src/domain/account_flag/AccountFlag.py` | `Actor`, `AuditEntry`, `Bool`, `IfaceKind`, `Interface`, `Permission`, `REQ_FRAUD_01`, `Resource`, `State` |
| `src/domain/card/Card.py` | `Actor`, `Permission` |
| `src/domain/transaction/Transaction.py` | `Permission`, `State` |
| `src/domain/user/User.py` | `Actor`, `Permission` |

---

### Task #84 — Admin Review of Flagged Transactions

**As a** admin
**I need** to review flagged suspicious transactions and decide whether to approve, reject, or escalate them
**So that** I can maintain system integrity and prevent fraud

### Details and Assumptions
* The system contains a mechanism for flagging transactions as suspicious
* Admin has the necessary permissions to view and act on flagged transactions
* Actions available are approve, reject, or escalate

### Acceptance Criteria

```gherkin
Given I am logged in as an admin
When I view a list of suspicious transactions
Then I can see each flagged transaction with its details

Given I am reviewing a suspicious transaction
When I select an action (approve, reject, or escalate)
Then the transaction status is updated accordingly
And the action is logged for audit purposes
```

**UML class diagram:** `experiments/project_11/class_diagram_84.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/account/Account.py` | `Actor`, `Permission` |
| `src/domain/account_flag/AccountFlag.py` | `Actor`, `AuditEntry`, `Permission` |
| `src/domain/card/Card.py` | `Actor`, `Permission` |
| `src/domain/transaction/Transaction.py` | `Permission` |
| `src/domain/user/User.py` | `Actor`, `Permission` |

---

### Task #85 — Admin Lock/Unlock Accounts

**As a** admin
**I need** to lock a user's account (e.g., due to suspicious activity) and later unlock it when the issue is resolved
**So that** I can manage user account security and access

### Details and Assumptions
* Admin has the ability to lock and unlock user accounts.
* The system tracks the reason for locking (e.g., suspicious activity).
* Unlocking restores full access to the user's account.

### Acceptance Criteria

```gherkin
Given a user account with suspicious activity
When the admin locks the account
Then the account is locked and the user cannot log in

Given a locked user account
When the admin resolves the issue and unlocks the account
Then the account is unlocked and the user can log in again
```

**UML class diagram:** `experiments/project_11/class_diagram_85.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/account/Account.py` | `Actor`, `Permission` |
| `src/domain/account_flag/AccountFlag.py` | `Actor`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/card/Card.py` | `Actor`, `Permission` |
| `src/domain/transaction/Transaction.py` | `Permission`, `State` |
| `src/domain/user/User.py` | `Actor`, `Permission`, `User` |

---

### Task #86 — Admin View Transaction History

**As a** admin
**I need** view the full transaction history of any user
**So that** aid in auditing and investigation

### Details and Assumptions
* The admin has access to a user management interface.
* Transaction history includes all financial or activity logs for a selected user.
* The system must support searching or selecting a specific user.

### Acceptance Criteria

```gherkin
Given I am logged in as an admin
When I select a user to view their transaction history
Then I should see a complete list of that user's transactions
```

**UML class diagram:** `experiments/project_11/class_diagram_86.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/account/Account.py` | `Actor`, `Permission` |
| `src/domain/account_flag/AccountFlag.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/card/Card.py` | `Actor`, `Permission` |
| `src/domain/transaction/Transaction.py` | `Permission`, `State`, `Transaction` |
| `src/domain/user/User.py` | `Actor`, `Permission` |

---

### Task #87 — Audit Log of Auth Attempts and State Changes

**As a** security auditor  
**I need** the system to log all authentication attempts (success/failure) and account state changes (lock/unlock)  
**So that** I can review and audit security events for compliance and threat detection  

### Details and Assumptions
* Logs should include timestamp, username, IP address, action type, and outcome.
* Logs must be stored in a secure, tamper-evident format.
* Retention period and access controls for logs are defined elsewhere.

### Acceptance Criteria

```gherkin
Given the system is operational
When a user attempts authentication (success or failure)
Then the system records the event with details (timestamp, username, IP, outcome)

Given the system is operational
When an account is locked or unlocked
Then the system records the state change with details (timestamp, username, action)
```

**UML class diagram:** `experiments/project_11/class_diagram_87.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/account/Account.py` | `Actor`, `Permission` |
| `src/domain/account_flag/AccountFlag.py` | `Actor`, `IfaceKind`, `Interface`, `Permission`, `State` |
| `src/domain/audit_log_entry/AuditLogEntry.py` | `AuditLogEntry` |
| `src/domain/card/Card.py` | `Actor`, `Permission` |
| `src/domain/transaction/Transaction.py` | `Permission`, `State` |
| `src/domain/user/User.py` | `Actor`, `Permission` |

---
