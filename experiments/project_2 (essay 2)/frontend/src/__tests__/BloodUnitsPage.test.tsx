import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { act } from 'react';

vi.mock('../api/services', () => ({
  listBloodUnits: vi.fn().mockResolvedValue([
    { id: 1, uniqueID: 'BLD-001', aboType: 'A', rhFactor: '+', collectionDate: '2025-01-01', expiryDate: '2025-02-12', status: 'available' },
  ]),
  createBloodUnit: vi.fn().mockResolvedValue({ id: 2, uniqueID: 'BLD-002', aboType: 'B', rhFactor: '-', collectionDate: '2025-02-01', expiryDate: '2025-03-15', status: 'available' }),
  deleteBloodUnit: vi.fn().mockResolvedValue(undefined),
}));

import BloodUnitsPage from '../pages/BloodUnitsPage';

describe('BloodUnitsPage', () => {
  it('renders blood units list', async () => {
    await act(async () => {
      render(<BloodUnitsPage />);
    });
    expect(screen.getByText('Blood Units')).toBeTruthy();
    expect(screen.getByText('BLD-001')).toBeTruthy();
    expect(screen.getByText('available')).toBeTruthy();
  });
});
