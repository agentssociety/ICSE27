import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import AccountsPage from '../pages/AccountsPage';

vi.mock('../api/services', () => ({
  listAccounts: vi.fn().mockResolvedValue({ data: [] }),
  createAccount: vi.fn().mockResolvedValue({}),
}));

describe('AccountsPage', () => {
  it('renders without crashing and shows accounts heading', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <AccountsPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Accounts')).toBeDefined();
  });
});
