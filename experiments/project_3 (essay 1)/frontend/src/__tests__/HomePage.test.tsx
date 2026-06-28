import { describe, it, expect, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

vi.mock('../api/services', () => ({
  listFlights: vi.fn().mockResolvedValue({ data: [] }),
  listRunways: vi.fn().mockResolvedValue({ data: [] }),
  listSlots: vi.fn().mockResolvedValue({ data: [] }),
}));

import HomePage from '../pages/HomePage';

describe('HomePage', () => {
  it('renders dashboard title', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <HomePage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Airport Runway Scheduling')).toBeDefined();
  });
});