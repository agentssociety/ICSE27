export interface Patient {
  id: number;
  username: string;
  authentication_id?: number;
}

export interface PatientCreate {
  id: number;
  username: string;
  authentication_id: number;
}

export interface PatientUpdate {
  id: number;
  username?: string;
  authentication_id?: number;
}

export interface Symptom {
  id: number;
  description: string;
  language: string;
  patientId: string;
  patient_id?: number;
}

export interface SymptomCreate {
  id: number;
  description: string;
  language: string;
  patientId: string;
  patient_id: number;
}

export interface SymptomUpdate {
  id: number;
  description?: string;
  language?: string;
  patientId?: string;
  patient_id?: number;
}

export interface SymptomRecord {
  id: number;
  recordId: string;
  symptomData: string;
  patientId: string;
  symptom_id?: number;
}

export interface SymptomRecordCreate {
  id: number;
  recordId: string;
  symptomData: string;
  patientId: string;
  symptom_id: number;
}

export interface SymptomRecordUpdate {
  id: number;
  recordId?: string;
  symptomData?: string;
  patientId?: string;
  symptom_id?: number;
}

export interface UserAuthenticationSystem {
  userId: string;
  sessionToken: string;
  patient_id?: number;
}

export interface UserAuthenticationSystemCreate {
  sessionToken: string;
  userId: string;
  patient_id: number;
}

export interface UserAuthenticationSystemUpdate {
  sessionToken?: string;
  userId?: string;
  patient_id?: number;
}

export interface Resource {
  id: number;
  owner_id?: number;
}

export interface ResourceCreate {
  id: number;
  owner_id: number;
}

export interface ResourceUpdate {
  id: number;
  owner_id?: number;
}

// UI-specific types for queue management
export type UrgencyLevel = 1 | 2 | 3 | 4 | 5;

export interface QueueItem {
  patient: Patient;
  symptom?: Symptom;
  symptomRecord?: SymptomRecord;
  urgency: UrgencyLevel;
  position: number;
  estimatedWaitTimeMinutes: number;
  registeredAt: string;
}