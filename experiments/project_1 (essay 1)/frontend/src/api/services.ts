import axios from 'axios';
import type { Patient, PatientQueue, QueueOverview, QueuePatientsResponse, RegisterPatientRequest, DequeueResponse } from '../types';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

export async function getQueueOverview(queueId: number = 1): Promise<QueueOverview> {
  const { data } = await api.get<QueueOverview>(`/dashboard/queue/${queueId}/overview`);
  return data;
}

export async function getQueuePatients(queueId: number = 1): Promise<Patient[]> {
  const { data } = await api.get<QueuePatientsResponse>(`/dashboard/queue/${queueId}/patients`);
  return data.patients ?? [];
}

export async function registerPatient(request: RegisterPatientRequest): Promise<Patient> {
  const { data } = await api.post<Patient>('/patients', request);
  return data;
}

export async function getPatient(patientId: number): Promise<Patient> {
  const { data } = await api.get<Patient>(`/patients/${patientId}`);
  return data;
}

export async function updatePatient(patientId: number, updates: Partial<Patient>): Promise<Patient> {
  const { data } = await api.put<Patient>(`/patients/${patientId}`, updates);
  return data;
}

export async function deletePatient(patientId: number): Promise<void> {
  await api.delete(`/patients/${patientId}`);
}

export async function dequeuePatient(queueId: number = 1): Promise<DequeueResponse> {
  // Backend has no dedicated dequeue endpoint. Fetch queue patients and delete the highest-priority one.
  const patients = await getQueuePatients(queueId);
  if (patients.length === 0) {
    return { patient: null, removed: false };
  }
  const sorted = [...patients].sort((a, b) => a.urgency_level - b.urgency_level);
  const top = sorted[0];
  await deletePatient(top.id);
  return { patient: top, removed: true };
}

export async function getPatientQueue(queueId: number): Promise<PatientQueue> {
  const { data } = await api.get<PatientQueue>(`/patient_queues/${queueId}`);
  return data;
}

export async function updatePatientQueue(queueId: number, updates: Partial<PatientQueue>): Promise<PatientQueue> {
  const { data } = await api.put<PatientQueue>(`/patient_queues/${queueId}`, updates);
  return data;
}

export async function deletePatientQueue(queueId: number): Promise<void> {
  await api.delete(`/patient_queues/${queueId}`);
}
