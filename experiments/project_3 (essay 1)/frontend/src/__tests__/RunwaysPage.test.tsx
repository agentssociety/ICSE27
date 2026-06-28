import { describe, it, expect, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

vi.mock('../api/services', () => ({
  listRunways: vi.fn().mockResolvedValue({ data: [] }),
  getRunwayTimetable: vi.fn(),
  createRunway: vi.fn(),
  deleteRunway: vi.fn(),
  updateRunway: vi.fn(),
}));

import RunwaysPage from '../pages/RunwaysPage';

describe('RunwaysPage', () => {
  it('renders runway management page', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <RunwaysPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Runway Management')).toBeDefined();
  });
});