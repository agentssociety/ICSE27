
import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import ProfilePage from '../pages/ProfilePage';

vi.mock('../api/services', () => ({
  listUsers: vi.fn().mockResolvedValue([{ id: 1, email: 'alice@test.com', name: 'Alice', accountStatus: 'active', isAuthenticated: true }]),
  listPosts: vi.fn().mockResolvedValue([]),
  listProfiles: vi.fn().mockResolvedValue([]),
  updateUser: vi.fn(),
}));

describe('ProfilePage', () => {
  it('renders without crashing', async () => {
    await act(async () => {
      render(<ProfilePage />);
    });
    expect(screen.getByText('Profile')).toBeInTheDocument();
  });
});
