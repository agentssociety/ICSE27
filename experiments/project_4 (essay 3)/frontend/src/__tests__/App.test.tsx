import { vi } from 'vitest';
import { act, render } from '@testing-library/react';
import App from '../App';

// Mock all API service calls that the DashboardPage uses (rendered at "/")
vi.mock('../api/services', () => ({
  listAccounts: vi.fn().mockResolvedValue({ data: [] }),
  listWithdrawals: vi.fn().mockResolvedValue({ data: { items: [], total: 0 } }),
  listFlaggedTransactions: vi.fn().mockResolvedValue({ data: { items: [], total: 0 } }),
}));

describe('App', () => {
  it('renders without crashing', async () => {
    await act(async () => {
      render(<App />)
    });
  });
});
