import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { act } from 'react';

vi.mock('../api/services', () => ({
  listReservations: vi.fn().mockResolvedValue([
    { id: 'res-001', bloodUnitId: 'BLD-001', transfusionRequestId: 'req-001', bloodUnit_id: 1, status: 'active' },
  ]),
  listBloodUnits: vi.fn().mockResolvedValue([
    { id: 1, uniqueID: 'BLD-001', aboType: 'A', rhFactor: '+', collectionDate: '2025-01-01', expiryDate: '2025-02-12', status: 'available' },
  ]),
  listTransfusionRequests: vi.fn().mockResolvedValue([
    { bloodType: 'A', rhFactor: '+', quantity: 2 },
  ]),
  createReservation: vi.fn().mockResolvedValue({ id: 'res-002', bloodUnitId: 'BLD-002', transfusionRequestId: 'req-002', bloodUnit_id: 2, status: 'active' }),
  deleteReservation: vi.fn().mockResolvedValue(undefined),
}));

import ReservationsPage from '../pages/ReservationsPage';

describe('ReservationsPage', () => {
  it('renders reservations list', async () => {
    await act(async () => {
      render(<ReservationsPage />);
    });
    expect(screen.getByText('Reservations')).toBeTruthy();
    expect(screen.getByText('Reservation #res-001')).toBeTruthy();
    expect(screen.getByText('active')).toBeTruthy();
  });
});
