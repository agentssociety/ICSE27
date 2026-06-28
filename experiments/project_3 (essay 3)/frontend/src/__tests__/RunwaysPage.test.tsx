import { describe, it, expect } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import RunwaysPage from '../pages/RunwaysPage';

vi.mock('../api/services', () => ({
  runwayApi: {
    getAll: vi.fn().mockResolvedValue([]),
    getById: vi.fn().mockResolvedValue({}),
    update: vi.fn().mockResolvedValue({}),
  },
  flightApi: {
    getAll: vi.fn().mockResolvedValue([]),
  },
  closeRunway: vi.fn().mockResolvedValue({ reassignedFlights: [] }),
}));

vi.mock('../components/Layout', () => ({
  default: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}));

describe('RunwaysPage', () => {
  it('renders the runways page with title', async () => {
    await act(async () => {
      render(
        <MemoryRouter>
          <RunwaysPage />
        </MemoryRouter>
      );
    });
    expect(await screen.findByText('Runways')).toBeInTheDocument();
  });
});