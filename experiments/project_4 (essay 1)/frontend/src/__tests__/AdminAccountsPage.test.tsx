import { describe, it, expect, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import AdminAccountsPage from '../pages/AdminAccountsPage';

vi.mock('../api/services', () => ({
  listAccounts: vi.fn().mockResolvedValue({ data: [] }),
  lockAccount: vi.fn().mockResolvedValue({}),
  unlockAccount: vi.fn().mockResolvedValue({}),
}));

describe('AdminAccountsPage', () => {
  it('renders manage accounts heading', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <AdminAccountsPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Manage Accounts')).toBeDefined();
  });
});