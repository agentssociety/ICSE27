import axios from 'axios';
import type {
  AccountCreate, AccountResponse, AccountUpdate,
  AccountFlagResponse,
  ActorCreate, ActorResponse, ActorUpdate,
  AuditEntryResponse,
  AuditLogEntryCreate, AuditLogEntryResponse, AuditLogEntryUpdate,
  CardCreate, CardResponse, CardUpdate,
  MoneyCreate, MoneyResponse, MoneyUpdate,
  PINCreate, PINResponse, PINUpdate,
  TransactionCreate, TransactionResponse, TransactionUpdate,
  UserCreate, UserResponse, UserUpdate,
  WithdrawalRecordCreate, WithdrawalRecordResponse,
  LoginRequest, LoginResponse
} from '../types';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

// ─── Health ───
export const healthCheck = () => api.get('/health');

// ─── Accounts ───
export const listAccounts = () => api.get<AccountResponse[]>('/accounts');
export const getAccount = (id: number) => api.get<AccountResponse>(`/accounts/${id}`);
export const createAccount = (data: AccountCreate) => api.post<AccountResponse>('/accounts', data);
export const updateAccount = (id: number, data: Partial<AccountUpdate>) => api.put<AccountResponse>(`/accounts/${id}`, data);
export const deleteAccount = (id: number) => api.delete(`/accounts/${id}`);

// ─── Account Flags ───
export const listAccountFlags = () => api.get<AccountFlagResponse[]>('/accounts/flags');

// ─── Actors ───
export const listActors = () => api.get<ActorResponse[]>('/actors');
export const getActor = (id: string) => api.get<ActorResponse>(`/actors/${id}`);
export const createActor = (data: ActorCreate) => api.post<ActorResponse>('/actors', data);
export const updateActor = (id: string, data: ActorUpdate) => api.put<ActorResponse>(`/actors/${id}`, data);

// ─── Audit Logs ───
export const listAuditLogs = () => api.get<AuditLogEntryResponse[]>('/audit_logs');
export const getAuditLog = (id: number) => api.get<AuditLogEntryResponse>(`/audit_logs/${id}`);

// ─── Cards ───
export const listCards = () => api.get<CardResponse[]>('/cards');
export const getCard = (id: number) => api.get<CardResponse>(`/cards/${id}`);
export const createCard = (data: CardCreate) => api.post<CardResponse>('/cards', data);
export const updateCard = (id: number, data: CardUpdate) => api.put<CardResponse>(`/cards/${id}`, data);
export const deleteCard = (id: number) => api.delete(`/cards/${id}`);

// ─── Moneys ───
export const listMoneys = () => api.get<MoneyResponse[]>('/moneys');
export const getMoney = (id: number) => api.get<MoneyResponse>(`/moneys/${id}`);
export const createMoney = (data: MoneyCreate) => api.post<MoneyResponse>('/moneys', data);

// ─── PINs ───
export const listPins = () => api.get<PINResponse[]>('/pins');
export const getPin = (id: number) => api.get<PINResponse>(`/pins/${id}`);
export const createPin = (data: PINCreate) => api.post<PINResponse>('/pins', data);
export const updatePin = (id: number, data: PINUpdate) => api.put<PINResponse>(`/pins/${id}`, data);
export const deletePin = (id: number) => api.delete(`/pins/${id}`);

// ─── Transactions ───
export const listTransactions = () => api.get<TransactionResponse[]>('/transactions');
export const getTransaction = (id: string) => api.get<TransactionResponse>(`/transactions/${id}`);
export const getTransactionsByUser = (userId: string) => api.get<TransactionResponse[]>(`/transactions/user/${userId}`);
export const listFlaggedTransactions = () => api.get<TransactionResponse[]>('/transactions/flagged');
export const createTransaction = (data: TransactionCreate) => api.post<TransactionResponse>('/transactions', data);
export const updateTransaction = (id: string, data: TransactionUpdate) => api.put<TransactionResponse>(`/transactions/${id}`, data);
export const deleteTransaction = (id: string) => api.delete(`/transactions/${id}`);

// ─── Users ───
export const listUsers = () => api.get<UserResponse[]>('/users');
export const getUser = (id: string) => api.get<UserResponse>(`/users/${id}`);
export const createUser = (data: UserCreate) => api.post<UserResponse>('/users', data);
export const updateUser = (id: string, data: UserUpdate) => api.put<UserResponse>(`/users/${id}`, data);
export const deleteUser = (id: string) => api.delete(`/users/${id}`);

// ─── Withdrawal Records ───
export const listWithdrawalRecords = () => api.get<WithdrawalRecordResponse[]>('/withdrawal_records');
export const getWithdrawalRecord = (id: number) => api.get<WithdrawalRecordResponse>(`/withdrawal_records/${id}`);
export const createWithdrawalRecord = (data: WithdrawalRecordCreate) => api.post<WithdrawalRecordResponse>('/withdrawal_records', data);

// ─── Auth (simulated: login via card + PIN lookup) ───
export const loginUser = async (data: LoginRequest): Promise<LoginResponse> => {
  try {
    const [cardsRes, pinsRes, usersRes] = await Promise.all([
      listCards(),
      listPins(),
      listUsers(),
    ]);
    const card = cardsRes.data.find(c => c.id === data.card_id);
    if (!card) return { success: false, message: 'Card not found' };
    const pin = pinsRes.data.find(p => p.id === data.pin_id);
    if (!pin) return { success: false, message: 'PIN not found' };
    const user = usersRes.data.find(u => u.card_id === data.card_id && u.pIN_id === data.pin_id);
    if (!user) return { success: false, message: 'Invalid card or PIN' };

    const accountRes = await getAccount(user.account_id!);
    if (accountRes.data.locked_reason) {
      return { success: false, message: `Account locked: ${accountRes.data.locked_reason}`, locked: true };
    }
    return { success: true, user: user, account: accountRes.data };
  } catch {
    return { success: false, message: 'Authentication error' };
  }
};

// ─── Admin: Lock/Unlock Account ───
export const lockAccount = async (accountId: number, reason: string) => {
  return updateAccount(accountId, { locked_reason: reason });
};

export const unlockAccount = async (accountId: number) => {
  return updateAccount(accountId, { locked_reason: '' });
};

// ─── Admin: Flagged transaction review actions ───
export const reviewFlaggedTransaction = async (transactionId: string, action: 'approve' | 'reject' | 'escalate', adminUserId: string) => {
  await updateTransaction(transactionId, { status_id: action === 'approve' ? 2 : action === 'reject' ? 3 : 4 });
};

// ─── Audit Log Helper ───
export const createAuditLog = (data: AuditLogEntryCreate) => {
  return api.post('/audit_logs', data).catch(() => {
    console.warn('Could not create audit log via POST');
  });
};
