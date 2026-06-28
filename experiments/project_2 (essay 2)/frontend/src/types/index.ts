export interface BloodUnitCreate {
  uniqueID: string;
  aboType: string;
  rhFactor: string;
  collectionDate: string;
}

export interface BloodUnitUpdate {
  uniqueID?: string;
  aboType?: string;
  rhFactor?: string;
  collectionDate?: string;
  status?: string;
}

export interface BloodUnit {
  id: number;
  uniqueID: string;
  aboType: string;
  rhFactor: string;
  collectionDate: string;
  expiryDate: string;
  status: string;
}

export interface TransfusionRequestDTO {
  bloodType: string;
  rhFactor: string;
  quantity: number;
}

export interface ValidationResult {
  isValid: boolean;
  errorMessage: string;
}

export interface StorageResult {
  success: boolean;
  requestId: string;
  errorMessage: string;
}

export interface SubmitResponse {
  success: boolean;
  message: string;
  requestId: string;
}

export interface ReservationCreate {
  bloodUnitId: string;
  transfusionRequestId: string;
  bloodUnit_id: number;
}

export interface ReservationUpdate {
  bloodUnitId?: string;
  transfusionRequestId?: string;
  bloodUnit_id?: number;
  status?: string;
}

export interface Reservation {
  id: string;
  bloodUnitId: string;
  transfusionRequestId: string;
  bloodUnit_id?: number;
  status?: string;
}

export interface StockLevel {
  aboType: string;
  rhFactor: string;
  count: number;
}
