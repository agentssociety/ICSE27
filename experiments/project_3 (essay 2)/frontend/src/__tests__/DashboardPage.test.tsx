import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import DashboardPage from '../pages/DashboardPage';

vi.mock('../api/services', () => ({
  listFlights: vi.fn().mockResolvedValue([]),
}));

describe('DashboardPage', () => {
  it('renders dashboard heading', async () => {
    await act(async () => {
      render(<MemoryRouter><DashboardPage /></MemoryRouter>);
    });
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
  });
});
