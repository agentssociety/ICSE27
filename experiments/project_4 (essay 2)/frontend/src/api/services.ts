// ============================================================
// API Service Layer - all backend calls
// ============================================================
import axios from "axios";
import type {
  LoginRequestDTO,
  LoginResponseDTO,
  UnlockRequestDTO,
  UnlockResponseDTO,
  AuthorizationRequest,
  AuthorizationResponse,
  AccountData,
  AuditLogEntryCreate,
  AuditLogEntryUpdate,
  AuditLogEntryResponse,
  TransactionCreateRequest,
  TransactionUpdateRequest,
  TransactionResponse,
  UserCreateRequest,
  UserUpdateRequest,
  UserResponse,
  CardCreateRequest,
  CardUpdateRequest,
  CardResponse,
  PinCreateRequest,
  PinUpdateRequest,
  PinResponse,
} from "../types";

const api = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
});

// --- Audit Log Endpoints ---
// Paths from contract: /audit_log_entrys/* (mounted with prefix /audit_log_entrys)

export const listAuditLogEntries = () =>
  api.get<AuditLogEntryResponse[]>("/audit_log_entrys").then((r) => r.data);

export const getAuditLogEntry = (id: string) =>
  api.get<AuditLogEntryResponse>(`/audit_log_entrys/${id}`).then((r) => r.data);

export const createAuditLogEntry = (data: AuditLogEntryCreate) =>
  api.post<AuditLogEntryResponse>("/audit_log_entrys", data).then((r) => r.data);

export const updateAuditLogEntry = (id: string, data: AuditLogEntryUpdate) =>
  api.put<AuditLogEntryResponse>(`/audit_log_entrys/${id}`, data).then((r) => r.data);

export const deleteAuditLogEntry = (id: string) =>
  api.delete(`/audit_log_entrys/${id}`).then((r) => r.data);

// --- Account Endpoints ---
// The account router exists but is NOT mounted in main.py.
// We define the helpers here for when it gets mounted.
// Hardcoding paths that the router would expose if mounted at root:

export const login = (data: LoginRequestDTO) =>
  api.post<LoginResponseDTO>("/login", data).then((r) => r.data);

export const unlockAccount = (data: UnlockRequestDTO) =>
  api.post<UnlockResponseDTO>("/unlock", data).then((r) => r.data);

export const authorizeTransaction = (data: AuthorizationRequest) =>
  api.post<AuthorizationResponse>("/authorize", data).then((r) => r.data);

export const getBalance = (accountId: string) =>
  api.get<AccountData>(`/${accountId}/balance`).then((r) => r.data);

// --- Transaction Endpoints ---
// Transaction router exists but not mounted
export const getTransaction = (id: string) =>
  api.get<TransactionResponse>(`/transactions/${id}`).then((r) => r.data);

export const updateTransaction = (id: string, data: TransactionUpdateRequest) =>
  api.put<TransactionResponse>(`/transactions/${id}`, data).then((r) => r.data);

export const deleteTransaction = (id: string) =>
  api.delete(`/transactions/${id}`).then((r) => r.data);

// --- User Endpoints ---
export const getUser = (id: string) =>
  api.get<UserResponse>(`/users/${id}`).then((r) => r.data);

export const updateUser = (id: string, data: UserUpdateRequest) =>
  api.put<UserResponse>(`/users/${id}`, data).then((r) => r.data);

export const deleteUser = (id: string) =>
  api.delete(`/users/${id}`).then((r) => r.data);

// --- Card Endpoints ---
export const getCard = (id: string) =>
  api.get<CardResponse>(`/cards/${id}`).then((r) => r.data);

export const updateCard = (id: string, data: CardUpdateRequest) =>
  api.put<CardResponse>(`/cards/${id}`, data).then((r) => r.data);

export const deleteCard = (id: string) =>
  api.delete(`/cards/${id}`).then((r) => r.data);

// --- PIN Endpoints ---
export const getPin = (id: string) =>
  api.get<PinResponse>(`/pins/${id}`).then((r) => r.data);

export const updatePin = (id: string, data: PinUpdateRequest) =>
  api.put<PinResponse>(`/pins/${id}`, data).then((r) => r.data);

export const deletePin = (id: string) =>
  api.delete(`/pins/${id}`).then((r) => r.data);