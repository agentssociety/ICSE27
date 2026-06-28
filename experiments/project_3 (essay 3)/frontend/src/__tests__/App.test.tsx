
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from '../App';

vi.mock('../api/services', () => ({
  flightApi: {
    getAll: vi.fn().mockResolvedValue([]),
  },
  slotApi: {
    getAll: vi.fn().mockResolvedValue([]),
  },
  runwayApi: {
    getAll: vi.fn().mockResolvedValue([]),
  },
}));

describe('App', () => {
  it('renders the dashboard page', async () => {
    render(<App />);
    expect(await screen.findByText('Dashboard')).toBeInTheDocument();
  });
});
