export interface FlightCreate {
  flightNumber: string;
  origin: string;
  destination: string;
  estimatedDepartureTime: string;
}

export interface FlightUpdate {
  flightNumber?: string;
  origin?: string;
  destination?: string;
  estimatedDepartureTime?: string;
}

export interface FlightResponse {
  id: number;
  flightNumber: string;
  origin: string;
  destination: string;
  estimatedDepartureTime: string;
}

export interface RunwayCreate {
  flight_id?: number | null;
}

export interface RunwayUpdate {
  flight_id?: number | null;
}

export interface RunwayResponse {
  id: string;
  flight_id?: number | null;
}

export interface SlotCreateRequest {
  startTime: string;
  endTime: string;
  flight_type?: string;
  duration?: string;
  gapAfter?: string;
}

export interface SlotUpdateRequest {
  startTime?: string;
  endTime?: string;
  flight_type?: string;
  duration?: string;
  gapAfter?: string;
}

export interface SlotResponse {
  id: number;
  startTime: string;
  endTime: string;
  flight_type: string;
  duration: string;
  gapAfter: string;
}

export interface ActorResponse {
  id: number;
}

export interface InterfaceResponse {
  id: number;
}

export interface ResourceResponse {
  id: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
}
