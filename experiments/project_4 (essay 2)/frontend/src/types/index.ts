export interface LoginRequestDTO {
  userId: string;
  pin: string;
}

export interface LoginResponseDTO {
  success: boolean;
  lockStatus: "LOCKED" | "UNLOCKED";
  message: string;
}

export interface UnlockRequestDTO {
  userId: string;
  adminId: string;
}

export interface UnlockResponseDTO {
  success: boolean;
  message: string;
}

export interface AuthorizationRequest {
  initiatorId: string;
  accountId: string;
  amount: number;
  permission: string;
  interfaceType: string;
}

export interface AuthorizationResponse {
  authorized: boolean;
  newBalance: number;
  newUsedToday: number;
  reason: string;
}

export interface AccountData {
  balance: number;
  dailyLimit: number;
  usedToday: number;
}

export interface AuditLogEntryCreate {
  eventType: string;
  userId: string;
  sourceIp: string;
  outcome: string;
}

export interface AuditLogEntryUpdate {
  eventType?: string;
  userId?: string;
  sourceIp?: string;
  outcome?: string;
}

export interface AuditLogEntryResponse {
  userId: string;
  eventType: string;
  sourceIp: string;
  outcome: string;
}

export interface TransactionCreateRequest {
  amount: number;
  accountId: string;
  userId: string;
}

export interface TransactionUpdateRequest {
  amount?: number;
  status?: string;
}

export interface TransactionResponse {
  id: string;
  amount: number;
  timestamp: string;
  accountId: string;
  status: string;
  userId: string;
}

export interface UserCreateRequest {
  name: string;
  email: string;
}

export interface UserUpdateRequest {
  name?: string;
  email?: string;
}

export interface UserResponse {
  id: string;
  name: string;
  email: string;
  is_active: boolean;
}

export interface CardCreateRequest {
  user_id: string;
  card_number: string;
}

export interface CardUpdateRequest {
  card_number?: string;
}

export interface CardResponse {
  id: string;
  user_id: string;
  card_number: string;
}

export interface PinCreateRequest {
  user_id: string;
  pin_code: string;
}

export interface PinUpdateRequest {
  pin_code?: string;
}

export interface PinResponse {
  id: string;
  user_id: string;
  pin_code: string;
}