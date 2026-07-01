
import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import AdminPage from '../pages/AdminPage';

vi.mock('../api/services', () => ({
  listUsers: vi.fn().mockResolvedValue([{ id: 1, email: 'admin@test.com', name: 'Admin', accountStatus: 'active', isAuthenticated: true }]),
  listAuditLogs: vi.fn().mockResolvedValue([]),
  listUserProfiles: vi.fn().mockResolvedValue([]),
  listReports: vi.fn().mockResolvedValue([]),
  listBlocks: vi.fn().mockResolvedValue([]),
  listRoles: vi.fn().mockResolvedValue([]),
  updateUserProfile: vi.fn(),
  deleteUser: vi.fn(),
  createAuditLog: vi.fn(),
}));

describe('AdminPage', () => {
  it('renders without crashing', async () => {
    await act(async () => {
      render(<AdminPage />);
    });
    expect(screen.getByText('Admin Panel')).toBeInTheDocument();
  });
});
