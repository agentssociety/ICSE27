import { describe, it, expect, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

vi.mock('../api/services', () => ({
  listFlights: vi.fn().mockResolvedValue({ data: [] }),
  createFlight: vi.fn(),
  deleteFlight: vi.fn(),
}));

import FlightsPage from '../pages/FlightsPage';

describe('FlightsPage', () => {
  it('renders flight registration page', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <FlightsPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Flight Registration')).toBeDefined();
  });
});