// Types derived from backend Pydantic schemas

export interface BloodUnitCreate {
  bloodType: string;
  rhFactor: string;
  donationDate: string;
}

export interface BloodUnitResponse {
  id: number;
  bloodType: string;
  rhFactor: string;
  donationDate: string;
  expirationDate?: string;
  isExpiring: boolean;
}

export interface TransfusionRequestCreate {
  patientName: string;
  bloodType: string;
  quantity: number;
  urgency: string;
}

export interface TransfusionRequestUpdate {
  patientName?: string;
  bloodType?: string;
  quantity?: number;
  urgency?: string;
}

export interface TransfusionRequestResponse {
  id: number;
  patientName: string;
  bloodType: string;
  quantity: number;
  urgency: string;
  status: string;
}

export interface ReservationCreate {
  bloodType: string;
  quantity: number;
  scheduledDate: string;
}

export interface ReservationResponse {
  id: number;
  bloodType: string;
  quantity: number;
  scheduledDate: string;
  status: string;
}

export interface InventoryDashboard {
  stock_summary: Record<string, number>;
  expiring_units_count: number;
  expiring_units: Array<{
    id: number;
    bloodType: string;
    rhFactor: string;
    expirationDate?: string;
  }>;
  pending_requests_count: number;
}
