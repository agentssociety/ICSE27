import { describe, it, expect, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import DashboardPage from '../pages/DashboardPage';

vi.mock('../api/services', () => ({
  listBloodUnits: vi.fn().mockResolvedValue([
    { id: 1, abo_rh_type: 'O+', collection_date: '2025-01-01', is_expired: false },
    { id: 2, abo_rh_type: 'A-', collection_date: '2025-01-15', is_expired: false },
  ]),
  listTransfusionRequests: vi.fn().mockResolvedValue([
    { id: '1', requestId: 'REQ-001', patientId: 'PAT-001', patientABORh: 'O+', bloodType: 'O+', patientID: 'PAT-001' },
  ]),
  getShortageAlerts: vi.fn().mockResolvedValue([]),
  checkExpiredUnits: vi.fn().mockResolvedValue([]),
}));

describe('DashboardPage', () => {
  it('renders the dashboard with stock levels and requests', async () => {
    await act(async () => {
      render(
        <MemoryRouter>
          <DashboardPage />
        </MemoryRouter>
      );
    });
    expect(screen.getByText('Inventory Dashboard')).toBeDefined();
    expect(screen.getByText('Current Stock Levels')).toBeDefined();
    expect(screen.getByText('Units Nearing Expiration')).toBeDefined();
    expect(screen.getByText('Open Transfusion Requests')).toBeDefined();
    // O+ appears multiple times, use getAllByText to confirm at least 2 occurrences
    expect(screen.getAllByText('O+').length).toBeGreaterThanOrEqual(2);
    expect(screen.getByText('REQ-001')).toBeDefined();
  });
});
