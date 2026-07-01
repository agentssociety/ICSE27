
import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import MessagesPage from '../pages/MessagesPage';

vi.mock('axios', () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: [] }),
    create: vi.fn().mockReturnThis(),
  },
  get: vi.fn().mockResolvedValue({ data: [] }),
}));

describe('MessagesPage', () => {
  it('renders without crashing', async () => {
    await act(async () => {
      render(<MessagesPage />);
    });
  });

  it('shows title after loading', async () => {
    await act(async () => {
      render(<MessagesPage />);
    });
    expect(screen.getByText('Messages')).toBeInTheDocument();
  });
});
