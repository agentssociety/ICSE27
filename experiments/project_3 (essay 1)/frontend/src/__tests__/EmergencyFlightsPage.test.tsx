import { describe, it, expect, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

vi.mock('../api/services', () => ({
  listFlights: vi.fn().mockResolvedValue({ data: [] }),
  listSlots: vi.fn().mockResolvedValue({ data: [] }),
  createSlot: vi.fn(),
}));

import EmergencyFlightsPage from '../pages/EmergencyFlightsPage';

describe('EmergencyFlightsPage', () => {
  it('renders emergency flight handling page', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <EmergencyFlightsPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Emergency Flight Handling')).toBeDefined();
  });
});