export interface Patient {
  id: number;
  patientId: string;
  patientQueue_id?: number;
  state: string;
  arrival_time?: string;
  urgency_level: number;
}

export interface PatientQueue {
  id: number;
  queueId: string;
}

export interface QueueOverview {
  queue_id: number;
  message: string;
  status: string;
}

export interface QueuePatientsResponse {
  queue_id: number;
  patients: Patient[];
}

export interface RegisterPatientRequest {
  patientId: string;
  urgency_level: number;
  state?: string;
  patientQueue_id?: number;
}

export interface DequeueResponse {
  patient: Patient | null;
  removed: boolean;
}
