export interface AccountCreate {
  failedAttempts?: number;
  balance?: number;
  daily_withdrawal_limit?: number;
  withdrawn_today?: number;
  locked_reason?: string;
}

export interface AccountUpdate {
  id?: number;
  failedAttempts?: number;
  balance?: number;
  daily_withdrawal_limit?: number;
  withdrawn_today?: number;
  locked_reason?: string;
}

export interface AccountResponse {
  id: number;
  failedAttempts: number;
  balance: number;
  daily_withdrawal_limit: number;
  withdrawn_today: number;
  locked_reason?: string;
}

export interface AccountFlagCreate {
  account_id?: number;
  transaction_id?: string;
}

export interface AccountFlagUpdate {
  account_id?: number;
  transaction_id?: string;
}

export interface AccountFlagResponse {
  id: number;
  account_id?: number;
  transaction_id?: string;
}

export interface ActorCreate {
  name: string;
}

export interface ActorUpdate {
  name?: string;
}

export interface ActorResponse {
  id: string;
  name: string;
}

export interface AuditEntryCreate {
  operation_id: number;
  recordedBy_id: number;
}

export interface AuditEntryUpdate {
  operation_id?: number;
  recordedBy_id?: number;
}

export interface AuditEntryResponse {
  id: number;
  operation_id?: number;
  recordedBy_id?: number;
}

export interface AuditLogEntryCreate {
  operation: string;
  timestamp: string;
  username: string;
  ip_address: string;
  outcome: string;
  user_id?: string;
  account_id?: number;
  action_type?: string;
}

export interface AuditLogEntryUpdate {
  operation?: string;
  timestamp?: string;
  username?: string;
  ip_address?: string;
  outcome?: string;
  user_id?: string;
  account_id?: number;
  action_type?: string;
}

export interface AuditLogEntryResponse {
  operation: string;
  timestamp: string;
  username: string;
  ip_address: string;
  outcome: string;
  user_id: string;
  account_id?: number;
  action_type?: string;
}

export interface CardCreate {
  owner_id: number;
  expiryDate?: string;
}

export interface CardUpdate {
  owner_id?: number;
  expiryDate?: string;
}

export interface CardResponse {
  id: number;
  owner_id?: number;
  expiryDate?: string;
}

export interface InterfaceCreate {
}

export interface InterfaceUpdate {
}

export interface InterfaceResponse {
  id: number;
}

export interface MoneyCreate {
  amount: number;
  currency?: string;
}

export interface MoneyUpdate {
  amount?: number;
  currency?: string;
}

export interface MoneyResponse {
  id: number;
  amount: number;
  currency: string;
}

export interface PINCreate {
  owner_id: number;
  user_id: number;
}

export interface PINUpdate {
  owner_id?: number;
  user_id?: number;
}

export interface PINResponse {
  id: number;
  owner_id?: number;
  user_id?: number;
}

export interface REQ_FRAUD_01Create {
  initiator_id: number;
  target_id: number;
  channel_id: number;
  pre_id: number;
  post_id: number;
}

export interface REQ_FRAUD_01Update {
  initiator_id?: number;
  target_id?: number;
  channel_id?: number;
  pre_id?: number;
  post_id?: number;
}

export interface REQ_FRAUD_01Response {
  id: number;
  initiator_id?: number;
  target_id?: number;
  channel_id?: number;
  pre_id?: number;
  post_id?: number;
}

export interface ResourceCreate {
  owner_id: number;
}

export interface ResourceUpdate {
  owner_id?: number;
}

export interface ResourceResponse {
  id: number;
  owner_id?: number;
}

export interface TransactionCreate {
  transaction_id?: string;
  amount_id: number;
  timestamp?: string;
  status_id: number;
}

export interface TransactionUpdate {
  transaction_id?: string;
  amount_id?: number;
  timestamp?: string;
  status_id?: number;
}

export interface TransactionResponse {
  transaction_id: string;
  amount_id?: number;
  timestamp: string;
  status_id?: number;
}

export interface UserCreate {
  userID: string;
  card_id: number;
  pIN_id: number;
  account_id: number;
}

export interface UserUpdate {
  userID?: string;
  card_id?: number;
  pIN_id?: number;
  account_id?: number;
}

export interface UserResponse {
  userID: string;
  card_id?: number;
  pIN_id?: number;
  account_id?: number;
}

export interface WithdrawalRecordCreate {
  transaction_id: string;
  amount_id: number;
}

export interface WithdrawalRecordUpdate {
  transaction_id?: string;
  amount_id?: number;
}

export interface WithdrawalRecordResponse {
  id: number;
  transaction_id: string;
  amount_id?: number;
}

export interface LoginRequest {
  card_id: number;
  pin_id: number;
}

export interface LoginResponse {
  success: boolean;
  user?: UserResponse;
  account?: AccountResponse;
  message?: string;
  locked?: boolean;
}

export interface AdminAction {
  transaction_id: string;
  action: 'approve' | 'reject' | 'escalate';
}