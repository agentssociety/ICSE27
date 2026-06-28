import axios from 'axios';
import type {
  FlightCreate, FlightUpdate, FlightResponse,
  SlotCreate, SlotUpdate, SlotResponse,
  RunwayCreate, RunwayUpdate, RunwayResponse,
  TimeSlotCreate, TimeSlotUpdate, TimeSlotResponse,
  AlternativeRunwayCreate, AlternativeRunwayUpdate, AlternativeRunwayResponse,
  OperationCreate, OperationUpdate, OperationResponse,
} from '../types';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

// --- Flight endpoints ---
export const listFlights = () =>
  api.get<FlightResponse[]>('/flights').then(r => r.data);

export const getFlight = (id: number) =>
  api.get<FlightResponse>(`/flights/${id}`).then(r => r.data);

export const createFlight = (data: FlightCreate) =>
  api.post<FlightResponse>('/flights', data).then(r => r.data);

export const updateFlight = (id: number, data: FlightUpdate) =>
  api.put<FlightResponse>(`/flights/${id}`, data).then(r => r.data);

export const deleteFlight = (id: number) =>
  api.delete(`/flights/${id}`).then(r => r.data);

// --- Slot endpoints ---
export const listSlots = () =>
  api.get<SlotResponse[]>('/slots').then(r => r.data);

export const getSlot = (id: number) =>
  api.get<SlotResponse>(`/slots/${id}`).then(r => r.data);

export const createSlot = (data: SlotCreate) =>
  api.post<SlotResponse>('/slots', data).then(r => r.data);

export const updateSlot = (id: number, data: SlotUpdate) =>
  api.put<SlotResponse>(`/slots/${id}`, data).then(r => r.data);

export const deleteSlot = (id: number) =>
  api.delete(`/slots/${id}`).then(r => r.data);

// --- Runway endpoints ---
export const listRunways = () =>
  api.get<RunwayResponse[]>('/runways').then(r => r.data);

export const getRunway = (id: number) =>
  api.get<RunwayResponse>(`/runways/${id}`).then(r => r.data);

export const createRunway = (data: RunwayCreate) =>
  api.post<RunwayResponse>('/runways', data).then(r => r.data);

export const updateRunway = (id: number, data: RunwayUpdate) =>
  api.put<RunwayResponse>(`/runways/${id}`, data).then(r => r.data);

export const deleteRunway = (id: number) =>
  api.delete(`/runways/${id}`).then(r => r.data);

// --- Time Slot endpoints ---
export const listTimeSlots = () =>
  api.get<TimeSlotResponse[]>('/time_slots').then(r => r.data);

export const getTimeSlot = (id: number) =>
  api.get<TimeSlotResponse>(`/time_slots/${id}`).then(r => r.data);

export const createTimeSlot = (data: TimeSlotCreate) =>
  api.post<TimeSlotResponse>('/time_slots', data).then(r => r.data);

export const updateTimeSlot = (id: number, data: TimeSlotUpdate) =>
  api.put<TimeSlotResponse>(`/time_slots/${id}`, data).then(r => r.data);

export const deleteTimeSlot = (id: number) =>
  api.delete(`/time_slots/${id}`).then(r => r.data);

// --- Alternative Runway endpoints ---
export const listAlternativeRunways = () =>
  api.get<AlternativeRunwayResponse[]>('/alternative_runways').then(r => r.data);

export const getAlternativeRunway = (id: number) =>
  api.get<AlternativeRunwayResponse>(`/alternative_runways/${id}`).then(r => r.data);

export const createAlternativeRunway = (data: AlternativeRunwayCreate) =>
  api.post<AlternativeRunwayResponse>('/alternative_runways', data).then(r => r.data);

export const updateAlternativeRunway = (id: number, data: AlternativeRunwayUpdate) =>
  api.put<AlternativeRunwayResponse>(`/alternative_runways/${id}`, data).then(r => r.data);

export const deleteAlternativeRunway = (id: number) =>
  api.delete(`/alternative_runways/${id}`).then(r => r.data);

// --- Operation endpoints ---
export const listOperations = () =>
  api.get<OperationResponse[]>('/operations').then(r => r.data);

export const getOperation = (id: number) =>
  api.get<OperationResponse>(`/operations/${id}`).then(r => r.data);

export const createOperation = (data: OperationCreate) =>
  api.post<OperationResponse>('/operations', data).then(r => r.data);

export const updateOperation = (id: number, data: OperationUpdate) =>
  api.put<OperationResponse>(`/operations/${id}`, data).then(r => r.data);

export const deleteOperation = (id: number) =>
  api.delete(`/operations/${id}`).then(r => r.data);