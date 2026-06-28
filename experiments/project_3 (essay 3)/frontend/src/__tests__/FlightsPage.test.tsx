import { describe, it, expect } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import FlightsPage from '../pages/FlightsPage';

vi.mock('../api/services', () => ({
  flightApi: {
    getAll: vi.fn().mockResolvedValue([]),
    create: vi.fn().mockResolvedValue({}),
    delete: vi.fn().mockResolvedValue({}),
  },
}));

vi.mock('../components/Layout', () => ({
  default: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}));

describe('FlightsPage', () => {
  it('renders the flights page with title', async () => {
    await act(async () => {
      render(
        <MemoryRouter>
          <FlightsPage />
        </MemoryRouter>
      );
    });
    expect(await screen.findByText('Flights')).toBeInTheDocument();
  });
});