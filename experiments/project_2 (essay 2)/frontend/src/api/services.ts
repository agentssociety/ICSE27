import axios from 'axios';
import type {
  BloodUnit,
  BloodUnitCreate,
  BloodUnitUpdate,
  TransfusionRequestDTO,
  ValidationResult,
  SubmitResponse,
  Reservation,
  ReservationCreate,
  ReservationUpdate,
} from '../types';

const api = axios.create({
  baseURL: '/api',
});

// === Blood Units ===
export function listBloodUnits() {
  return api.get<BloodUnit[]>('/blood_units').then((r) => r.data);
}

export function getBloodUnit(id: number) {
  return api.get<BloodUnit>(`/blood_units/${id}`).then((r) => r.data);
}

export function createBloodUnit(data: BloodUnitCreate) {
  return api.post<BloodUnit>('/blood_units', data).then((r) => r.data);
}

export function updateBloodUnit(id: number, data: BloodUnitUpdate) {
  return api.put<BloodUnit>(`/blood_units/${id}`, data).then((r) => r.data);
}

export function deleteBloodUnit(id: number) {
  return api.delete<void>(`/blood_units/${id}`).then((r) => r.data);
}

// === Transfusion Requests ===
export function validateTransfusionRequest(data: TransfusionRequestDTO) {
  return api.post<ValidationResult>('/transfusion_requests/validate', data).then((r) => r.data);
}

export function submitTransfusionRequest(data: TransfusionRequestDTO) {
  return api.post<SubmitResponse>('/transfusion_requests', data).then((r) => r.data);
}

export function getTransfusionRequest(requestId: string) {
  return api.get<SubmitResponse>(`/transfusion_requests/${requestId}`).then((r) => r.data);
}

export function listTransfusionRequests() {
  return api.get<TransfusionRequestDTO[]>('/transfusion_requests').then((r) => r.data);
}

// === Reservations ===
export function listReservations() {
  return api.get<Reservation[]>('/reservations').then((r) => r.data);
}

export function getReservation(id: string) {
  return api.get<Reservation>(`/reservations/${id}`).then((r) => r.data);
}

export function createReservation(data: ReservationCreate) {
  return api.post<Reservation>('/reservations', data).then((r) => r.data);
}

export function updateReservation(id: string, data: ReservationUpdate) {
  return api.put<Reservation>(`/reservations/${id}`, data).then((r) => r.data);
}

export function deleteReservation(id: string) {
  return api.delete<void>(`/reservations/${id}`).then((r) => r.data);
}
