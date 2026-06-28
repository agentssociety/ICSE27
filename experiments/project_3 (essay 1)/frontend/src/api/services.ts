import axios from 'axios';
import type {
  FlightCreate, FlightResponse, FlightUpdate,
  SlotCreate, SlotResponse, SlotUpdate,
  RunwayCreate, RunwayResponse, RunwayUpdate, RunwayTimetableResponse,
  EmergencyFlightCreate, EmergencyFlightResponse, EmergencyFlightUpdate,
  SeparationRuleCreate, SeparationRuleResponse, SeparationRuleUpdate,
  TrafficDataCreate, TrafficDataResponse, TrafficDataUpdate,
  AircraftCreate, AircraftResponse, AircraftUpdate,
  InterfaceCreate, InterfaceResponse,
  OperationResponse,
  OperationSlotResponse,
  StateResponse,
  ResourceResponse,
  PermissionResponse
} from '../types';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

// ===== Flights =====
export const listFlights = () => api.get<FlightResponse[]>('/flights');
export const getFlight = (id: number) => api.get<FlightResponse>(`/flights/${id}`);
export const createFlight = (data: FlightCreate) => api.post<FlightResponse>('/flights', data);
export const updateFlight = (id: number, data: FlightUpdate) => api.put<FlightResponse>(`/flights/${id}`, data);
export const deleteFlight = (id: number) => api.delete(`/flights/${id}`);

// ===== Slots =====
export const listSlots = () => api.get<SlotResponse[]>('/slots');
export const getSlot = (id: number) => api.get<SlotResponse>(`/slots/${id}`);
export const createSlot = (data: SlotCreate) => api.post<SlotResponse>('/slots', data);
export const updateSlot = (id: number, data: SlotUpdate) => api.put<SlotResponse>(`/slots/${id}`, data);
export const deleteSlot = (id: number) => api.delete(`/slots/${id}`);

// ===== Runways =====
export const listRunways = () => api.get<RunwayResponse[]>('/runways');
export const getRunway = (id: string) => api.get<RunwayResponse>(`/runways/${id}`);
export const createRunway = (data: RunwayCreate) => api.post<RunwayResponse>('/runways', data);
export const updateRunway = (id: string, data: RunwayUpdate) => api.put<RunwayResponse>(`/runways/${id}`, data);
export const deleteRunway = (id: string) => api.delete(`/runways/${id}`);
export const getRunwayTimetable = (id: string) => api.get<RunwayTimetableResponse>(`/runways/${id}/timetable`);

// ===== Emergency Flights =====
export const listEmergencyFlights = () => api.get<EmergencyFlightResponse[]>('/emergency_flights');
export const getEmergencyFlight = (id: string) => api.get<EmergencyFlightResponse>(`/emergency_flights/${id}`);
export const createEmergencyFlight = (data: EmergencyFlightCreate) => api.post<EmergencyFlightResponse>('/emergency_flights', data);
export const updateEmergencyFlight = (id: string, data: EmergencyFlightUpdate) => api.put<EmergencyFlightResponse>(`/emergency_flights/${id}`, data);
export const deleteEmergencyFlight = (id: string) => api.delete(`/emergency_flights/${id}`);

// ===== Separation Rules =====
export const listSeparationRules = () => api.get<SeparationRuleResponse[]>('/separation_rules');
export const getSeparationRule = (id: number) => api.get<SeparationRuleResponse>(`/separation_rules/${id}`);
export const createSeparationRule = (data: SeparationRuleCreate) => api.post<SeparationRuleResponse>('/separation_rules', data);
export const updateSeparationRule = (id: number, data: SeparationRuleUpdate) => api.put<SeparationRuleResponse>(`/separation_rules/${id}`, data);
export const deleteSeparationRule = (id: number) => api.delete(`/separation_rules/${id}`);

// ===== Traffic Data =====
export const listTrafficDatas = () => api.get<TrafficDataResponse[]>('/traffic_datas');
export const getTrafficData = (id: number) => api.get<TrafficDataResponse>(`/traffic_datas/${id}`);
export const createTrafficData = (data: TrafficDataCreate) => api.post<TrafficDataResponse>('/traffic_datas', data);
export const updateTrafficData = (id: number, data: TrafficDataUpdate) => api.put<TrafficDataResponse>(`/traffic_datas/${id}`, data);
export const deleteTrafficData = (id: number) => api.delete(`/traffic_datas/${id}`);

// ===== Aircraft =====
export const listAircrafts = () => api.get<AircraftResponse[]>('/aircrafts');
export const getAircraft = (id: number) => api.get<AircraftResponse>(`/aircrafts/${id}`);
export const createAircraft = (data: AircraftCreate) => api.post<AircraftResponse>('/aircrafts', data);
export const updateAircraft = (id: number, data: AircraftUpdate) => api.put<AircraftResponse>(`/aircrafts/${id}`, data);
export const deleteAircraft = (id: number) => api.delete(`/aircrafts/${id}`);

// ===== Operations =====
export const listOperations = () => api.get<OperationResponse[]>('/operations');
export const getOperation = (id: number) => api.get<OperationResponse>(`/operations/${id}`);

// ===== Operation Slots =====
export const listOperationSlots = () => api.get<OperationSlotResponse[]>('/operation_slots');
export const getOperationSlot = (id: number) => api.get<OperationSlotResponse>(`/operation_slots/${id}`);

// ===== States =====
export const listStates = () => api.get<StateResponse[]>('/states');
export const getState = (id: number) => api.get<StateResponse>(`/states/${id}`);

// ===== Resources =====
export const listResources = () => api.get<ResourceResponse[]>('/resources');
export const getResource = (id: number) => api.get<ResourceResponse>(`/resources/${id}`);

// ===== Permissions =====
export const listPermissions = () => api.get<PermissionResponse[]>('/permissions');
export const getPermission = (id: number) => api.get<PermissionResponse>(`/permissions/${id}`);

// ===== Interfaces =====
export const listInterfaces = () => api.get<InterfaceResponse[]>('/interfaces');
export const getInterface = (id: number) => api.get<InterfaceResponse>(`/interfaces/${id}`);
export const createInterface = (data: InterfaceCreate) => api.post<InterfaceResponse>('/interfaces', data);

export default api;