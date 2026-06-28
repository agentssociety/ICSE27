import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { act } from 'react';

vi.mock('../api/services', () => ({
  listBloodUnits: vi.fn().mockResolvedValue([
    { id: 1, uniqueID: 'BLD-001', aboType: 'A', rhFactor: '+', collectionDate: '2025-01-01', expiryDate: '2025-02-12', status: 'available' },
    { id: 2, uniqueID: 'BLD-002', aboType: 'O', rhFactor: '-', collectionDate: '2025-02-01', expiryDate: '2025-03-15', status: 'available' },
  ]),
  listTransfusionRequests: vi.fn().mockResolvedValue([
    { bloodType: 'A', rhFactor: '+', quantity: 2 },
  ]),
}));

import DashboardPage from '../pages/DashboardPage';

describe('DashboardPage', () => {
  it('renders stock levels and open requests', async () => {
    await act(async () => {
      render(<DashboardPage />);
    });
    expect(screen.getByText('Blood Bank Dashboard')).toBeTruthy();
    expect(screen.getByText('Low Stock Alerts')).toBeTruthy();
    expect(screen.getAllByText(/A\+/).length).toBeGreaterThan(0);
    expect(screen.getByText('Pending')).toBeTruthy();
  });
});
