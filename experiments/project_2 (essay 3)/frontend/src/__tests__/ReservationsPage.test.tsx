import { describe, it, expect, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import ReservationsPage from '../pages/ReservationsPage';

vi.mock('../api/services', () => ({
  listReservations: vi.fn().mockResolvedValue([
    { id: 'res-1', request_id: 1, unit_id: 2 },
  ]),
  createReservation: vi.fn(),
  deleteReservation: vi.fn(),
}));

describe('ReservationsPage', () => {
  it('renders the reservations page with list', async () => {
    await act(async () => {
      render(
        <MemoryRouter>
          <ReservationsPage />
        </MemoryRouter>
      );
    });
    expect(screen.getByText('Reservation System')).toBeDefined();
    expect(screen.getByText('res-1')).toBeDefined();
  });
});
