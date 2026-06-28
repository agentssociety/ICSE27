import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import SlotsPage from '../pages/SlotsPage';

vi.mock('../api/services', () => ({
  listSlots: vi.fn().mockResolvedValue([]),
  createSlot: vi.fn(),
  deleteSlot: vi.fn(),
  listFlights: vi.fn().mockResolvedValue([]),
  listRunways: vi.fn().mockResolvedValue([]),
}));

describe('SlotsPage', () => {
  it('renders slot allocation heading', async () => {
    await act(async () => {
      render(<MemoryRouter><SlotsPage /></MemoryRouter>);
    });
    expect(screen.getByText('Slot Allocation')).toBeInTheDocument();
  });
});
