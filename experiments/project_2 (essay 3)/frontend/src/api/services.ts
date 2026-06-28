import axios from 'axios';
import type {
  BloodUnit, BloodUnitCreate, BloodUnitUpdate,
  TransfusionRequest, TransfusionRequestCreate, TransfusionRequestUpdate,
  Reservation, ReservationCreate, ReservationUpdate,
  BloodType, BloodTypeCreate, BloodTypeUpdate,
  PatientDetail,
  Actor,
  Resource, ResourceCreate, ResourceUpdate,
} from '../types';

const api = axios.create({
  baseURL: '/api',
});

// Blood Units
export const listBloodUnits = () => api.get<BloodUnit[]>('/blood_units').then(r => r.data);
export const getBloodUnit = (id: number) => api.get<BloodUnit>(`/blood_units/${id}`).then(r => r.data);
export const createBloodUnit = (data: BloodUnitCreate) => api.post<BloodUnit>('/blood_units', data).then(r => r.data);
export const updateBloodUnit = (id: number, data: BloodUnitUpdate) => api.put<BloodUnit>(`/blood_units/${id}`, data).then(r => r.data);
export const deleteBloodUnit = (id: number) => api.delete(`/blood_units/${id}`).then(r => r.data);

// Transfusion Requests
export const listTransfusionRequests = () => api.get<TransfusionRequest[]>('/transfusion_requests').then(r => r.data);
export const getTransfusionRequest = (id: string) => api.get<TransfusionRequest>(`/transfusion_requests/${id}`).then(r => r.data);
export const createTransfusionRequest = (data: TransfusionRequestCreate) => api.post<TransfusionRequest>('/transfusion_requests', data).then(r => r.data);
export const updateTransfusionRequest = (id: string, data: TransfusionRequestUpdate) => api.put<TransfusionRequest>(`/transfusion_requests/${id}`, data).then(r => r.data);
export const deleteTransfusionRequest = (id: string) => api.delete(`/transfusion_requests/${id}`).then(r => r.data);

// Reservations
export const listReservations = () => api.get<Reservation[]>('/reservations').then(r => r.data);
export const getReservation = (id: string) => api.get<Reservation>(`/reservations/${id}`).then(r => r.data);
export const createReservation = (data: ReservationCreate) => api.post<Reservation>('/reservations', data).then(r => r.data);
export const updateReservation = (id: string, data: ReservationUpdate) => api.put<Reservation>(`/reservations/${id}`, data).then(r => r.data);
export const deleteReservation = (id: string) => api.delete(`/reservations/${id}`).then(r => r.data);

// Blood Types
export const listBloodTypes = () => api.get<BloodType[]>('/blood_types').then(r => r.data);
export const getBloodType = (id: number) => api.get<BloodType>(`/blood_types/${id}`).then(r => r.data);
export const createBloodType = (data: BloodTypeCreate) => api.post<BloodType>('/blood_types', data).then(r => r.data);
export const updateBloodType = (id: number, data: BloodTypeUpdate) => api.put<BloodType>(`/blood_types/${id}`, data).then(r => r.data);
export const deleteBloodType = (id: number) => api.delete(`/blood_types/${id}`).then(r => r.data);

// Patient Details
export const listPatientDetails = () => api.get<PatientDetail[]>('/patient_details').then(r => r.data);
export const getPatientDetail = (id: number) => api.get<PatientDetail>(`/patient_details/${id}`).then(r => r.data);

// Actors
export const listActors = () => api.get<Actor[]>('/actors').then(r => r.data);
export const getActor = (id: number) => api.get<Actor>(`/actors/${id}`).then(r => r.data);
export const createActor = () => api.post<Actor>('/actors').then(r => r.data);
export const updateActor = (id: number) => api.put<Actor>(`/actors/${id}`).then(r => r.data);
export const deleteActor = (id: number) => api.delete(`/actors/${id}`).then(r => r.data);

// Resources
export const listResources = () => api.get<Resource[]>('/resources').then(r => r.data);
export const getResource = (id: number) => api.get<Resource>(`/resources/${id}`).then(r => r.data);
export const createResource = (data: ResourceCreate) => api.post<Resource>('/resources', data).then(r => r.data);
export const updateResource = (id: number, data: ResourceUpdate) => api.put<Resource>(`/resources/${id}`, data).then(r => r.data);
export const deleteResource = (id: number) => api.delete(`/resources/${id}`).then(r => r.data);

// Expiration check
export const checkExpiredUnits = async (): Promise<BloodUnit[]> => {
  const units = await listBloodUnits();
  return units.filter(u => u.is_expired);
};

// Shortage check
export interface ShortageAlert {
  abo_rh_type: string;
  count: number;
}
export const getShortageAlerts = async (): Promise<ShortageAlert[]> => {
  const units = await listBloodUnits();
  const counts: Record<string, number> = {};
  units.filter(u => !u.is_expired).forEach(u => {
    counts[u.abo_rh_type] = (counts[u.abo_rh_type] || 0) + 1;
  });
  return Object.entries(counts)
    .filter(([_, count]) => count < 5)
    .map(([abo_rh_type, count]) => ({ abo_rh_type, count }));
};

// Compatibility matching
export const getCompatibleUnits = async (patientABORh: string): Promise<BloodUnit[]> => {
  const units = await listBloodUnits();
  const compatibleTypes = getCompatibleTypes(patientABORh);
  return units.filter(u => !u.is_expired && compatibleTypes.includes(u.abo_rh_type));
};

function getCompatibleTypes(patientType: string): string[] {
  if (patientType === 'O-') return ['O-'];
  if (patientType === 'O+') return ['O-', 'O+'];
  if (patientType === 'A-') return ['O-', 'A-'];
  if (patientType === 'A+') return ['O-', 'O+', 'A-', 'A+'];
  if (patientType === 'B-') return ['O-', 'B-'];
  if (patientType === 'B+') return ['O-', 'O+', 'B-', 'B+'];
  if (patientType === 'AB-') return ['O-', 'A-', 'B-', 'AB-'];
  if (patientType === 'AB+') return ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'];
  return [];
}
