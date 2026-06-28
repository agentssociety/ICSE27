import axios from 'axios';

// --- Interfaces matching backend Pydantic DTOs ---

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

export interface AuthenticationAttemptResponse {
  id: string;
  user_id: string;
  outcome: string;
  method: string;
  ip_address: string;
  timestamp: string;
}

export interface AuthenticationAttemptCreate {
  id: string;
  user_id: string;
  outcome?: string;
  method?: string;
  ip_address?: string;
  timestamp: string;
}

export interface AuthenticationSessionResponse {
  id: number;
  sessionId: string;
  user_id?: number;
  card_id?: number;
}

export interface AuthenticationSessionCreate {
  id: number;
  sessionId: string;
  user_id: number;
  card_id: number;
}

export interface CardResponse {
  id: number;
  cardNumber: string;
  user_id?: number;
  authenticationAttempt_id?: number;
}

export interface CardCreate {
  id: number;
  cardNumber: string;
  user_id: number;
  authenticationAttempt_id: number;
}

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

export interface TransactionLogResponse {
  id: number;
  logRecord: string;
}

export interface SuspiciousPatternResponse {
  id: number;
  active: boolean;
  withdrawalTransaction_id?: number;
}

export interface LockoutRecordResponse {
  id: number;
  operation: string;
}

export interface LockoutNotificationResponse {
  id: number;
  lockout_id?: number;
}

export interface FailedAttemptResponse {
  id: number;
  operation: string;
}

// Additional interfaces for endpoints typed as any (PINs, etc.)
export interface PinResponse {
  id: number;
}

export interface ActorResponse {
  id: string;
}

export interface AccountBalanceResponse {
  id: number;
}

export interface StorageStateResponse {
  id: number;
  capacity: number;
  used: number;
}

export interface LoadAlertResponse {
  id: number;
  channel: string;
  highLoad: boolean;
}

export interface UserAccountResponse {
  id: number;
}

export interface WithdrawalLimitResponse {
  id: number;
}

export interface WithdrawalRequestResponse {
  id: number;
}

export interface TransactionStateChangeResponse {
  id: number;
}

// --- Service functions (unchanged except for corrected types) ---

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

// --- Health ---
export const checkHealth = () => api.get('/health');

// --- Accounts (mapped to /account_balances) ---
export const listAccounts = () => api.get<AccountResponse[]>('/account_balances');
export const getAccount = (id: string | number) => api.get<AccountResponse>(`/account_balances/${id}`);
export const createAccount = (data: AccountCreateRequest) => api.post<AccountResponse>('/account_balances', data);
export const updateAccount = (id: string | number, data: AccountUpdateRequest) => api.put<AccountResponse>(`/account_balances/${id}`, data);
export const deleteAccount = (id: string | number) => api.delete(`/account_balances/${id}`);

// --- Users ---
export const listUsers = () => api.get<UserListResponse>('/users');
export const getUser = (userId: string | number) => api.get<UserResponse>(`/users/${userId}`);
export const createUser = (data: UserCreateRequest) => api.post<UserResponse>('/users', data);
export const updateUser = (userId: string | number, data: UserUpdateRequest) => api.put<UserResponse>(`/users/${userId}`, data);
export const deleteUser = (userId: string | number) => api.delete(`/users/${userId}`);
export const deactivateUser = (userId: string | number) => api.post<UserResponse>(`/users/${userId}/deactivate`);
export const activateUser = (userId: string | number) => api.post<UserResponse>(`/users/${userId}/activate`);

// --- Authentication Sessions ---
export const listAuthenticationSessions = () => api.get<AuthenticationSessionResponse[]>('/authentication_sessions');
export const getAuthenticationSession = (id: string | number) => api.get<AuthenticationSessionResponse>(`/authentication_sessions/${id}`);
export const createAuthenticationSession = (data: AuthenticationSessionCreate) => api.post<AuthenticationSessionResponse>('/authentication_sessions', data);
export const updateAuthenticationSession = (id: string | number, data: any) => api.put<AuthenticationSessionResponse>(`/authentication_sessions/${id}`, data);
export const deleteAuthenticationSession = (id: string | number) => api.delete(`/authentication_sessions/${id}`);

// --- Authentication Attempts ---
export const listAuthenticationAttempts = () => api.get<AuthenticationAttemptResponse[]>('/authentication_attempts');
export const getAuthenticationAttempt = (id: string | number) => api.get<AuthenticationAttemptResponse>(`/authentication_attempts/${id}`);
export const createAuthenticationAttempt = (data: AuthenticationAttemptCreate) => api.post<AuthenticationAttemptResponse>('/authentication_attempts', data);
export const deleteAuthenticationAttempt = (id: string | number) => api.delete(`/authentication_attempts/${id}`);

// --- Cards ---
export const listCards = () => api.get<CardResponse[]>('/cards');
export const getCard = (id: string | number) => api.get<CardResponse>(`/cards/${id}`);
export const createCard = (data: CardCreate) => api.post<CardResponse>('/cards', data);
export const updateCard = (id: string | number, data: any) => api.put<CardResponse>(`/cards/${id}`, data);
export const deleteCard = (id: string | number) => api.delete(`/cards/${id}`);

// --- PINs ---
export const listPins = () => api.get<PinResponse[]>('/pins');
export const getPin = (id: string | number) => api.get<PinResponse>(`/pins/${id}`);
export const createPin = (data: any) => api.post<PinResponse>('/pins', data);
export const updatePin = (id: string | number, data: any) => api.put<PinResponse>(`/pins/${id}`, data);
export const deletePin = (id: string | number) => api.delete(`/pins/${id}`);

// --- Daily Withdrawal Limits (mapped to /account_balances) ---
export const listDailyWithdrawalLimits = () => api.get<DailyWithdrawalLimitResponse[]>('/account_balances');
export const getDailyWithdrawalLimit = (id: string | number) => api.get<DailyWithdrawalLimitResponse>(`/account_balances/${id}`);
export const createDailyWithdrawalLimit = (data: DailyWithdrawalLimitCreateRequest) => api.post<DailyWithdrawalLimitResponse>('/account_balances', data);
export const updateDailyWithdrawalLimit = (id: string | number, data: any) => api.put<DailyWithdrawalLimitResponse>(`/account_balances/${id}`, data);
export const deleteDailyWithdrawalLimit = (id: string | number) => api.delete(`/account_balances/${id}`);

// --- Withdrawal Transactions ---
export const listWithdrawals = () => api.get<WithdrawalListResponse>('/withdrawal_transactions');
export const getWithdrawal = (id: string | number) => api.get<WithdrawalResponse>(`/withdrawal_transactions/${id}`);
export const createWithdrawal = (data: WithdrawalCreateRequest) => api.post<WithdrawalResponse>('/withdrawal_transactions', data);
export const failWithdrawal = (id: string | number) => api.post<WithdrawalResponse>(`/withdrawal_transactions/${id}/fail`);

// --- Flagged Transactions ---
export const listFlaggedTransactions = () => api.get<FlaggedTransactionListResponse>('/flagged_transactions');
export const getFlaggedTransaction = (id: string | number) => api.get<FlaggedTransactionResponse>(`/flagged_transactions/${id}`);
export const reviewFlaggedTransaction = (id: string | number, data: FlagReviewRequest) => api.post<FlaggedTransactionResponse>(`/flagged_transactions/${id}/review`, data);

// --- Transaction Logs ---
export const listTransactionLogs = () => api.get<TransactionLogResponse[]>('/transaction_logs');
export const getTransactionLog = (id: string | number) => api.get<TransactionLogResponse>(`/transaction_logs/${id}`);

// --- Suspicious Patterns ---
export const listSuspiciousPatterns = () => api.get<SuspiciousPatternResponse[]>('/suspicious_patterns');
export const getSuspiciousPattern = (id: string | number) => api.get<SuspiciousPatternResponse>(`/suspicious_patterns/${id}`);

// --- Lockout Records ---
export const listLockoutRecords = () => api.get<LockoutRecordResponse[]>('/lockout_records');
export const getLockoutRecord = (id: string | number) => api.get<LockoutRecordResponse>(`/lockout_records/${id}`);

// --- Lockout Notifications ---
export const listLockoutNotifications = () => api.get<LockoutNotificationResponse[]>('/lockout_notifications');
export const getLockoutNotification = (id: string | number) => api.get<LockoutNotificationResponse>(`/lockout_notifications/${id}`);

// --- Failed Attempts ---
export const listFailedAttempts = () => api.get<FailedAttemptResponse[]>('/failed_attempts');
export const getFailedAttempt = (id: string | number) => api.get<FailedAttemptResponse>(`/failed_attempts/${id}`);

// --- Account Balances ---
export const listAccountBalances = () => api.get<AccountBalanceResponse[]>('/account_balances');
export const getAccountBalance = (id: string | number) => api.get<AccountBalanceResponse>(`/account_balances/${id}`);

// --- Admin Routes ---
export const adminListWithdrawals = () => api.get<WithdrawalListResponse>('/admin/withdrawals');
export const adminGetWithdrawal = (withdrawalId: string | number) => api.get<WithdrawalResponse>(`/admin/withdrawals/${withdrawalId}`);
export const adminListFlaggedTransactions = () => api.get<FlaggedTransactionListResponse>('/admin/flagged-transactions');
export const adminGetFlaggedTransaction = (flaggedId: string | number) => api.get<FlaggedTransactionResponse>(`/admin/flagged-transactions/${flaggedId}`);
export const adminReviewFlaggedTransaction = (flaggedId: string | number, data: FlagReviewRequest) => api.post<FlaggedTransactionResponse>(`/admin/flagged-transactions/${flaggedId}/review`, data);