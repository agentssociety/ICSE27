import axios from 'axios';
import type { PatientCreate, PatientUpdate, PatientResponse, DashboardItem } from '../types';

const api = axios.create({
  baseURL: '/api',
});

export async function listPatients(): Promise<PatientResponse[]> {
  const { data } = await api.get<PatientResponse[]>('/v1/patients');
  return data;
}

export async function getPatient(id: number): Promise<PatientResponse> {
  const { data } = await api.get<PatientResponse>(`/v1/patients/${id}`);
  return data;
}

export async function createPatient(patient: PatientCreate): Promise<PatientResponse> {
  const { data } = await api.post<PatientResponse>('/v1/patients', patient);
  return data;
}

export async function updatePatient(id: number, patient: PatientUpdate): Promise<PatientResponse> {
  const { data } = await api.put<PatientResponse>(`/v1/patients/${id}`, patient);
  return data;
}

export async function deletePatient(id: number): Promise<void> {
  await api.delete(`/v1/patients/${id}`);
}

export async function getDashboard(): Promise<DashboardItem[]> {
  const { data } = await api.get<DashboardItem[]>('/v1/patients/dashboard');
  return data;
}
