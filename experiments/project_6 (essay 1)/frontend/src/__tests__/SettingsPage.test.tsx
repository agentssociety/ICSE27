
import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import SettingsPage from '../pages/SettingsPage';

vi.mock('../api/services', () => ({
  listNotificationPreferences: vi.fn().mockResolvedValue([]),
  listUsers: vi.fn().mockResolvedValue([{ id: 1, email: 'test@test.com', name: 'Test User', accountStatus: 'active', isAuthenticated: true }]),
  updateNotificationPreference: vi.fn(),
  updateUser: vi.fn(),
  deleteUser: vi.fn().mockResolvedValue(undefined),
}));

describe('SettingsPage', () => {
  it('renders without crashing', async () => {
    await act(async () => {
      render(<SettingsPage />);
    });
    expect(screen.getByText('Settings')).toBeInTheDocument();
  });
});
