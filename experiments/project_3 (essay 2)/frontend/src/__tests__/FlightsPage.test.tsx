import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import FlightsPage from '../pages/FlightsPage';

vi.mock('../api/services', () => ({
  listFlights: vi.fn().mockResolvedValue([]),
  createFlight: vi.fn(),
  updateFlight: vi.fn(),
  deleteFlight: vi.fn(),
}));

describe('FlightsPage', () => {
  it('renders flight management heading', async () => {
    await act(async () => {
      render(<MemoryRouter><FlightsPage /></MemoryRouter>);
    });
    expect(screen.getByText('Flight Management')).toBeInTheDocument();
  });
});
