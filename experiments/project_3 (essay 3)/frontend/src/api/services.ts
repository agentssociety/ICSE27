
import axios from 'axios';
import type {
  FlightCreate,
  FlightUpdate,
  FlightResponse,
  RunwayCreate,
  RunwayUpdate,
  RunwayResponse,
  SlotCreateRequest,
  SlotUpdateRequest,
  SlotResponse,
  ActorResponse,
  InterfaceResponse,
  ResourceResponse,
} from '../types';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

// === Flight Services ===
export const flightApi = {
  getAll: () => api.get<FlightResponse[]>('/flights').then(r => r.data),
  getById: (id: number) => api.get<FlightResponse>(`/flights/${id}`).then(r => r.data),
  create: (data: FlightCreate) => api.post<FlightResponse>('/flights', data).then(r => r.data),
  update: (id: number, data: FlightUpdate) => api.put<FlightResponse>(`/flights/${id}`, data).then(r => r.data),
  delete: (id: number) => api.delete(`/flights/${id}`).then(r => r.data),
};

// === Runway Services ===
export const runwayApi = {
  getAll: () => api.get<RunwayResponse[]>('/runways').then(r => r.data),
  getById: (id: string) => api.get<RunwayResponse>(`/runways/${id}`).then(r => r.data),
  create: (data: RunwayCreate) => api.post<RunwayResponse>('/runways', data).then(r => r.data),
  update: (id: string, data: RunwayUpdate) => api.put<RunwayResponse>(`/runways/${id}`, data).then(r => r.data),
  delete: (id: string) => api.delete(`/runways/${id}`).then(r => r.data),
};

// === Slot Services ===
export const slotApi = {
  getAll: () => api.get<SlotResponse[]>('/slots').then(r => r.data),
  getById: (id: number) => api.get<SlotResponse>(`/slots/${id}`).then(r => r.data),
  create: (data: SlotCreateRequest) => api.post<SlotResponse>('/slots', data).then(r => r.data),
  update: (id: number, data: SlotUpdateRequest) => api.put<SlotResponse>(`/slots/${id}`, data).then(r => r.data),
  delete: (id: number) => api.delete(`/slots/${id}`).then(r => r.data),
};

// === Actor / Interface / Resource Services ===
export const actorApi = {
  getAll: () => api.get<ActorResponse[]>('/actors').then(r => r.data),
};

export const interfaceApi = {
  getAll: () => api.get<InterfaceResponse[]>('/interfaces').then(r => r.data),
};

export const resourceApi = {
  getAll: () => api.get<ResourceResponse[]>('/resources').then(r => r.data),
};

// === Health Check ===
export const healthApi = {
  check: () => api.get('/health').then(r => r.data),
};

// === Complex Operations (multi-step) ===

/** Allocate a 5-minute slot with a 3-minute gap after it */
export const createStandardSlot = (data: {
  startTime: string;
  flight_type?: string;
}) => {
  const start = new Date(data.startTime);
  const end = new Date(start.getTime() + 5 * 60000); // 5 minutes

  return slotApi.create({
    startTime: start.toISOString(),
    endTime: end.toISOString(),
    duration: '5m',
    gapAfter: '3m',
    flight_type: data.flight_type,
  });
};

/** Handle emergency flight: assign immediate slot and re-queue others */
export const handleEmergencyFlight = async (emergencyFlightId: number) => {
  const allSlots = await slotApi.getAll();
  const now = new Date().toISOString();

  const emergencySlot = await slotApi.create({
    startTime: now,
    endTime: new Date(Date.now() + 5 * 60000).toISOString(),
    flight_type: 'emergency',
    duration: '5m',
    gapAfter: '3m',
  });

  const nonEmergency = allSlots.filter(s => s.flight_type !== 'emergency');
  const reorderedSlots = [emergencySlot, ...nonEmergency];

  return {
    emergencySlot,
    reorderedSlots,
  };
};

/** Close a runway: reassign flights and mark delayed if > 60 min */
export const closeRunway = async (
  runwayId: string,
  alternateRunwayId: string
) => {
  const runway = await runwayApi.getById(runwayId);
  const alternate = await runwayApi.getById(alternateRunwayId);

  const allFlights = await flightApi.getAll();

  const reassignedFlights = [];
  for (const flight of allFlights) {
    await runwayApi.update(alternateRunwayId, { flight_id: flight.id });
    reassignedFlights.push(flight);
  }

  return { reassignedFlights };
};

export default api;
