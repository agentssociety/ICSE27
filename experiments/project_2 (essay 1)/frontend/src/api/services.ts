import axios from "axios";
import {
  BloodUnitCreate,
  BloodUnitResponse,
  TransfusionRequestCreate,
  TransfusionRequestUpdate,
  TransfusionRequestResponse,
  ReservationCreate,
  ReservationResponse,
  InventoryDashboard,
} from "../types";

const api = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
});

// Blood Units
export const listBloodUnits = async (): Promise<BloodUnitResponse[]> => {
  const response = await api.get<BloodUnitResponse[]>("/blood-units");
  return response.data;
};

export const createBloodUnit = async (data: BloodUnitCreate): Promise<BloodUnitResponse> => {
  const response = await api.post<BloodUnitResponse>("/blood-units", data);
  return response.data;
};

export const deleteBloodUnit = async (id: number): Promise<void> => {
  await api.delete(`/blood-units/${id}`);
};

// Transfusion Requests
export const listTransfusionRequests = async (): Promise<TransfusionRequestResponse[]> => {
  const response = await api.get<TransfusionRequestResponse[]>("/transfusion-requests");
  return response.data;
};

export const createTransfusionRequest = async (data: TransfusionRequestCreate): Promise<TransfusionRequestResponse> => {
  const response = await api.post<TransfusionRequestResponse>("/transfusion-requests", data);
  return response.data;
};

export const updateTransfusionRequest = async (id: number, data: TransfusionRequestUpdate): Promise<TransfusionRequestResponse> => {
  const response = await api.put<TransfusionRequestResponse>(`/transfusion-requests/${id}`, data);
  return response.data;
};

export const deleteTransfusionRequest = async (id: number): Promise<void> => {
  await api.delete(`/transfusion-requests/${id}`);
};

// Reservations
export const listReservations = async (): Promise<ReservationResponse[]> => {
  const response = await api.get<ReservationResponse[]>("/reservations");
  return response.data;
};

export const createReservation = async (data: ReservationCreate): Promise<ReservationResponse> => {
  const response = await api.post<ReservationResponse>("/reservations", data);
  return response.data;
};

export const deleteReservation = async (id: number): Promise<void> => {
  await api.delete(`/reservations/${id}`);
};

// Dashboard
export const getInventoryDashboard = async (): Promise<InventoryDashboard> => {
  const response = await api.get<InventoryDashboard>("/dashboard/dashboard");
  return response.data;
};
