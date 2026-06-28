import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import RunwaysPage from '../pages/RunwaysPage';

vi.mock('../api/services', () => ({
  listRunways: vi.fn().mockResolvedValue([]),
  createRunway: vi.fn(),
  updateRunway: vi.fn(),
  deleteRunway: vi.fn(),
}));

describe('RunwaysPage', () => {
  it('renders runway management heading', async () => {
    await act(async () => {
      render(<MemoryRouter><RunwaysPage /></MemoryRouter>);
    });
    expect(screen.getByText('Runway Management')).toBeInTheDocument();
  });
});
