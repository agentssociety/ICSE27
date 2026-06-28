import { describe, it, expect, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import BloodUnitsPage from '../pages/BloodUnitsPage';

vi.mock('../api/services', () => ({
  listBloodUnits: vi.fn().mockResolvedValue([
    { id: 1, abo_rh_type: 'A+', collection_date: '2025-02-01', is_expired: false },
  ]),
  createBloodUnit: vi.fn(),
  deleteBloodUnit: vi.fn(),
}));

describe('BloodUnitsPage', () => {
  it('renders the blood units page with list', async () => {
    await act(async () => {
      render(
        <MemoryRouter>
          <BloodUnitsPage />
        </MemoryRouter>
      );
    });
    expect(screen.getByText('Blood Unit Tracking')).toBeDefined();
    expect(screen.getByText('A+')).toBeDefined();
  });
});
