import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import UsersPage from '../pages/UsersPage';

vi.mock('../api/services', () => ({
  listUsers: vi.fn().mockResolvedValue({ data: { items: [], total: 0 } }),
  createUser: vi.fn().mockResolvedValue({}),
  deactivateUser: vi.fn().mockResolvedValue({}),
  activateUser: vi.fn().mockResolvedValue({}),
  deleteUser: vi.fn().mockResolvedValue({}),
}));

describe('UsersPage', () => {
  it('renders without crashing and shows users heading', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <UsersPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Users')).toBeDefined();
  });
});
