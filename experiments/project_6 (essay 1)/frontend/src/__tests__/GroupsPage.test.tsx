
import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import GroupsPage from '../pages/GroupsPage';

vi.mock('../api/services', () => ({
  listGroups: vi.fn().mockResolvedValue([]),
  listGroupMemberships: vi.fn().mockResolvedValue([]),
  listJoinRequests: vi.fn().mockResolvedValue([]),
  createGroupMembership: vi.fn(),
  createJoinRequest: vi.fn(),
}));

describe('GroupsPage', () => {
  it('renders without crashing', async () => {
    await act(async () => {
      render(<GroupsPage />);
    });
    expect(screen.getByText('Groups')).toBeInTheDocument();
  });
});
