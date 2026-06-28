// === Auto-generated from backend DTO contracts ===
// Maps backend types: str/UUID/datetime → string, int/float → number, bool → boolean

// --- Account ---
export interface AccountResponse {
  id: number;
  account_id: string;
  balance: number;
  locked: boolean;
  failed_attempt_count: number;
}

export interface AccountCreateRequest {
  account_id: string;
  balance?: number;
  locked?: boolean;
  failed_attempt_count?: number;
}

export interface AccountUpdateRequest {
  account_id?: string;
  balance?: number;
  locked?: boolean;
  failed_attempt_count?: number;
}

// --- User ---
export interface UserResponse {
  id: string;
  username: string;
  email: string;
  role: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface UserListResponse {
  items: UserResponse[];
  total: number;
}

export interface UserCreateRequest {
  username: string;
  email: string;
  password_hash: string;
  role?: string;
}

export interface UserUpdateRequest {
  username?: string;
  email?: string;
  password_hash?: string;
  role?: string;
}

// --- Authentication Attempt ---
export interface AuthenticationAttemptResponse {
  id: string;
  user_id: string;
  outcome: string;
  method: string;
  ip_address: string;
  timestamp: string;
}

export interface AuthenticationAttemptCreate {
  user_id: string;
  outcome?: string;
  method?: string;
  ip_address?: string;
  id: string;
  timestamp: string;
}

// --- Authentication Session ---
export interface AuthenticationSessionResponse {
  id: number;
  sessionId: string;
  user_id?: number;
  card_id?: number;
}

export interface AuthenticationSessionCreate {
  sessionId: string;
  user_id: number;
  card_id: number;
  id: number;
}

// --- Card ---
export interface CardResponse {
  id: number;
  cardNumber: string;
  user_id?: number;
  authenticationAttempt_id?: number;
}

export interface CardCreate {
  cardNumber: string;
  user_id: number;
  authenticationAttempt_id: number;
  id: number;
}

// --- PIN ---
export interface PinResponse {
  id: number;
}

// --- Daily Withdrawal Limit ---
export interface DailyWithdrawalLimitResponse {
  id: number;
  account_id: string;
  daily_limit: number;
  used_today: number;
}

export interface DailyWithdrawalLimitCreateRequest {
  account_id: string;
  daily_limit?: number;
  used_today?: number;
}

// --- Withdrawal Transaction ---
export interface WithdrawalResponse {
  id: string;
  account_id: string;
  amount: number;
  status: string;
  timestamp: string;
}

export interface WithdrawalListResponse {
  items: WithdrawalResponse[];
  total: number;
}

export interface WithdrawalCreateRequest {
  account_id: string;
  amount: number;
}

// --- Flagged Transaction ---
export interface FlaggedTransactionResponse {
  id: string;
  withdrawal_id: string;
  reason: string;
  flagged_at: string;
  reviewed_by?: string;
  status: string;
}

export interface FlaggedTransactionListResponse {
  items: FlaggedTransactionResponse[];
  total: number;
}

export interface FlagReviewRequest {
  reviewer_id: string;
}

// --- Transaction Log ---
export interface TransactionLogResponse {
  id: number;
  logRecord: string;
}

// --- Suspicious Pattern ---
export interface SuspiciousPatternResponse {
  id: number;
  active: boolean;
  withdrawalTransaction_id?: number;
}

// --- Lockout Record ---
export interface LockoutRecordResponse {
  id: number;
  operation: string;
}

// --- Lockout Notification ---
export interface LockoutNotificationResponse {
  id: number;
  lockout_id?: number;
}

// --- Failed Attempt ---
export interface FailedAttemptResponse {
  id: number;
  operation: string;
}

// --- Account Balance ---
export interface AccountBalanceResponse {
  id: number;
}

// --- Withdrawal Limit ---
export interface WithdrawalLimitResponse {
  id: number;
}

// --- Storage State ---
export interface StorageStateResponse {
  id: number;
  capacity: number;
  used: number;
}

// --- Audit Log Resource ---
export interface AuditLogResourceResponse {
  id: number;
  resourceId: string;
}

// --- Actor ---
export interface ActorResponse {
  id: string;
}

// --- User Account ---
export interface UserAccountResponse {
  id: number;
}

// --- Transaction State Change ---
export interface TransactionStateChangeResponse {
  id: number;
}

// --- Withdrawal Request ---
export interface WithdrawalRequestResponse {
  id: number;
}