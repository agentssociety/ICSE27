export interface BloodUnit {
  id: number;
  abo_rh_type: string;
  collection_date: string;
  is_expired?: boolean;
}

export interface BloodUnitCreate {
  abo_rh_type: string;
  collection_date: string;
}

export interface BloodUnitUpdate {
  id: number;
  abo_rh_type?: string;
  collection_date?: string;
  is_expired?: boolean;
}

export interface TransfusionRequest {
  id: string;
  requestId: string;
  patientId: string;
  patientABORh: string;
  bloodType: string;
  patientID: string;
}

export interface TransfusionRequestCreate {
  requestId: string;
  patientId: string;
  patientABORh: string;
  bloodType: string;
  patientID: string;
}

export interface TransfusionRequestUpdate {
  id: string;
  requestId?: string;
  patientId?: string;
  patientABORh?: string;
  bloodType?: string;
  patientID?: string;
}

export interface Reservation {
  id: string;
  request_id?: number;
  unit_id?: number;
}

export interface ReservationCreate {
  request_id: number;
  unit_id: number;
}

export interface ReservationUpdate {
  id: string;
  request_id?: number;
  unit_id?: number;
}

export interface BloodType {
  id: number;
  bloodUnit_id?: number;
  transfusionRequest_id?: number;
}

export interface BloodTypeCreate {
  bloodUnit_id: number;
  transfusionRequest_id: number;
}

export interface BloodTypeUpdate {
  id: number;
  bloodUnit_id?: number;
  transfusionRequest_id?: number;
}

export interface PatientDetail {
  id: number;
}

export interface Actor {
  id: number;
}

export interface Resource {
  id: number;
  owner_id?: number;
}

export interface ResourceCreate {
  owner_id: number;
}

export interface ResourceUpdate {
  id: number;
  owner_id?: number;
}
