from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime, timedelta

if TYPE_CHECKING:
    from src.domain.account import Account, Admin, Resource
    from src.domain.user import User

"""
Domain layer for the Transaction domain class

Package: domain.transaction
Layer: domain
Related tasks: #90, #92, #93
Requirement coverage:
- Enforce daily transaction limits
- Detect Suspicious Transaction Patterns
- Admin Interface for Flagged Transactions Review
"""

RAPID_WITHDRAWAL_THRESHOLD_SECONDS = 5
MAX_RAPID_WITHDRAWALS = 3


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"
    EXECUTE = "execute"


class State(Enum):
    PRE_IDLE = "pre_idle"
    POST_1 = "post_1"
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    RESOLVED = "resolved"


class TransactionStatus(Enum):
    NORMAL = "normal"
    FLAGGED = "flagged"
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    INVESTIGATING = "investigating"


class FlaggedTransactionStatus(Enum):
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    RESOLVED = "resolved"


@dataclass
class Transaction:
    id: str
    amount: Decimal
    timestamp: datetime
    accountId: str
    status: TransactionStatus
    user: User

    def initiate(self, amount: Any, account: Account) -> Transaction:
        # Create a new transaction with the given amount
        return Transaction(
            id=str(uuid4()),
            amount=Decimal(str(amount)),
            timestamp=datetime.utcnow(),
            accountId=account,
            status=TransactionStatus.NORMAL,
            user=self.user,
        )

    def markFlagged(self, flagId: str) -> None:
        self.status = TransactionStatus.FLAGGED


@dataclass
class FlaggedTransaction:
    transactionId: str
    flagTime: datetime
    reviewStatus: FlaggedTransactionStatus
    flagReason: str
    status: TransactionStatus

    def create(self, transaction: Transaction) -> FlaggedTransaction:
        return FlaggedTransaction(
            transactionId=transaction.id,
            flagTime=datetime.utcnow(),
            reviewStatus=FlaggedTransactionStatus.PENDING,
            flagReason="Suspicious pattern detected: multiple rapid withdrawals",
            status=TransactionStatus.FLAGGED,
        )

    def changeStatus(self, newStatus: FlaggedTransactionStatus) -> None:
        self.reviewStatus = newStatus


@dataclass
class FraudAnalyst:
    analystId: str
    permissions: list[Permission]


@dataclass
class System:
    permissions: list[Permission] = field(default_factory=lambda: [p for p in Permission])
    transactions: list[Transaction] = field(default_factory=list)
    flaggedTransactions: list[FlaggedTransaction] = field(default_factory=list)

    def checkFrequencyAndSpeed(self, accountId: str, timeframe: Any) -> bool:
        """Detect suspicious patterns: multiple rapid withdrawals from same account."""
        # Get transactions for this account within the last N seconds
        now = datetime.utcnow()
        cutoff = now - timedelta(seconds=RAPID_WITHDRAWAL_THRESHOLD_SECONDS)
        recent_txs = [
            t for t in self.transactions
            if t.accountId == accountId and t.timestamp >= cutoff
        ]
        # If there are more than MAX_RAPID_WITHDRAWALS, flag as suspicious
        return len(recent_txs) >= MAX_RAPID_WITHDRAWALS

    def getPendingFlaggedTransactions(self) -> list[FlaggedTransaction]:
        return [
            ft for ft in self.flaggedTransactions
            if ft.reviewStatus == FlaggedTransactionStatus.PENDING
        ]

    def updateFlaggedTransactionStatus(self, flagId: str, newStatus: FlaggedTransactionStatus) -> None:
        for ft in self.flaggedTransactions:
            if ft.transactionId == flagId:
                ft.changeStatus(newStatus)
                break

    def resolveFlaggedTransaction(self, flagId: str, resolution: str) -> None:
        self.updateFlaggedTransactionStatus(flagId, FlaggedTransactionStatus.RESOLVED)

    def logOutageEvent(self, details: Any) -> None:
        pass

    def startFallbackBuffer(self, tx: Transaction) -> None:
        pass

    def waitForNetworkRecovery(self, timeout: Any) -> None:
        pass

    def clearBuffer(self) -> None:
        pass

    def alertITTeam(self, outageEvent: Any) -> None:
        pass

    def persistBufferToLocalStorage(self) -> None:
        pass

    def checkCurrentLoad(self) -> Any:
        return 0

    def activateThrottling(self, policy: Any) -> None:
        pass

    def processBatch(self, transactions: list[Transaction]) -> None:
        for tx in transactions:
            self.processTransaction(tx)

    def processTransaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)
        # Check for suspicious patterns
        if self.checkFrequencyAndSpeed(transaction.accountId, None):
            ft = FlaggedTransaction.create(None, transaction)
            self.flaggedTransactions.append(ft)

    def checkPermission(self, initiator: Any, resource: Resource) -> bool:
        return True


@dataclass
class Actor:
    permissions: set[Permission]
    actorId: str
    transaction: Transaction
    account: Account
    note_mayPerform_assignment: str

    def getActorByCard(self, cardData: str) -> Actor:
        return Actor(
            permissions={Permission.READ},
            actorId=str(uuid4()),
            transaction=self.transaction,
            account=self.account,
        )

    def mayPerform(self, grant_Admin: Any) -> bool:
        return Permission.ADMIN in self.permissions

    def getPermissions(self, actorId: str) -> Permission:
        return Permission.READ

    def hasPermission(self, actor: Any, Write: Any) -> bool:
        return Permission.WRITE in self.permissions


@dataclass
class SystemAdministrator:
    note_right_of_SystemAdministrator: str
    id: UUID
    amount: Decimal
    timestamp: Any
    owner: Actor
    accessibleTo: list[Actor]

    def setStatus(self, newStatus: TransactionStatus) -> None:
        pass


@dataclass
class TransactionId:
    pass


@dataclass
class TransactionCreatedEvent:
    pass


@dataclass
class TransactionUpdatedEvent:
    pass
