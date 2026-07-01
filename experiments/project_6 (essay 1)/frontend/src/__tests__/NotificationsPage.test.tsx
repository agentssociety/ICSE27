
import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import NotificationsPage from '../pages/NotificationsPage';

vi.mock('../api/services', () => ({
  listNotifications: vi.fn().mockResolvedValue([]),
  listUsers: vi.fn().mockResolvedValue([]),
}));

describe('NotificationsPage', () => {
  it('renders without crashing', async () => {
    await act(async () => {
      render(<NotificationsPage />);
    });
    expect(screen.getByText('Notifications')).toBeInTheDocument();
  });
});
