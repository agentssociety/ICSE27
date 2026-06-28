export interface FlightCreate {
  flightNumber: string;
  aircraftType: string;
}

export interface FlightUpdate {
  flightNumber?: string;
  aircraftType?: string;
}

export interface FlightResponse {
  id: number;
  flightNumber: string;
  aircraftType: string;
}

export interface SlotCreate {
  resource_id?: number;
  isAvailable?: boolean;
  time?: number;
}

export interface SlotUpdate {
  resource_id?: number;
  isAvailable?: boolean;
  time?: number;
}

export interface SlotResponse {
  id: number;
  resource_id?: number;
  isAvailable: boolean;
  time: number;
}

export interface RunwayCreate {
  capacity: number;
  configuration: string;
  slot_id?: number;
}

export interface RunwayUpdate {
  capacity?: number;
  configuration?: string;
  slot_id?: number;
}

export interface RunwayResponse {
  id: string;
  capacity: number;
  configuration: string;
  slot_id?: number;
}

export interface TimetableEntry {
  slot_id?: number;
  slot_time?: number;
  flight_id?: number;
  flight_number?: string;
  aircraft_type?: string;
  status?: string;
}

export interface RunwayTimetableResponse {
  runway_id: string;
  runway_status?: string;
  entries?: TimetableEntry[];
}

export interface EmergencyFlightCreate {
  flight_id: number;
  slot_id?: number;
}

export interface EmergencyFlightUpdate {
  flight_id?: number;
  slot_id?: number;
}

export interface EmergencyFlightResponse {
  id: string;
  flight_id?: number;
  slot_id?: number;
}

export interface SeparationRuleCreate {
  wakeTurbulenceSeparation: Record<string, number>;
}

export interface SeparationRuleUpdate {
  wakeTurbulenceSeparation?: Record<string, number>;
}

export interface SeparationRuleResponse {
  id: number;
  wakeTurbulenceSeparation: Record<string, number>;
}

export interface TrafficDataCreate {
  runwayLoads: Record<string, number>;
}

export interface TrafficDataUpdate {
  runwayLoads?: Record<string, number>;
}

export interface TrafficDataResponse {
  id: number;
  runwayLoads: Record<string, number>;
}

export interface AircraftCreate {
  type: string;
  size: string;
}

export interface AircraftUpdate {
  type?: string;
  size?: string;
}

export interface AircraftResponse {
  id: number;
  type: string;
  size: string;
}

export interface InterfaceCreate {
  kind: string;
  encrypted: boolean;
  authenticated: boolean;
}

export interface InterfaceUpdate {
  kind?: string;
  encrypted?: boolean;
  authenticated?: boolean;
}

export interface InterfaceResponse {
  id: number;
  kind: string;
  encrypted: boolean;
  authenticated: boolean;
}

export interface OperationResponse {
  id: number;
  initiator_id?: number;
  grant_id?: number;
  pre_id?: number;
  post_id?: number;
}

export interface OperationSlotResponse {
  id: number;
  op_id?: number;
  slot_id?: number;
}

export interface StateResponse {
  id: number;
  description: string;
}

export interface ResourceResponse {
  id: number;
  owner_id?: number;
  slot_id?: number;
}

export interface PermissionResponse {
  id: number;
}
