export interface PatientCreate {
  id?: number;
  symptoms: string;
  urgencyLevel: number;
  queuePosition: number;
  arrivalTime: string;
  urgency: string;
}

export interface PatientUpdate {
  id?: number;
  symptoms?: string;
  urgencyLevel?: number;
  queuePosition?: number;
  arrivalTime?: string;
  urgency?: string;
}

export interface PatientResponse {
  id: number;
  symptoms: string;
  urgencyLevel: number;
  queuePosition: number;
  arrivalTime: string;
  urgency: string;
}

export interface DashboardItem {
  patient_id: number;
  symptoms: string;
  urgency_level: number;
  urgency: string;
  queue_position: number;
  estimated_wait_minutes: number;
  arrival_time: string;
}
