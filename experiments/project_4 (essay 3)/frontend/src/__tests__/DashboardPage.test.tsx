import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import DashboardPage from '../pages/DashboardPage';

// Mock all API services the dashboard uses
vi.mock('../api/services', () => ({
  listAccounts: vi.fn().mockResolvedValue({ data: [] }),
  listWithdrawals: vi.fn().mockResolvedValue({ data: { items: [], total: 0 } }),
  listFlaggedTransactions: vi.fn().mockResolvedValue({ data: { items: [], total: 0 } }),
}));

describe('DashboardPage', () => {
  it('renders without crashing and shows dashboard title', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <DashboardPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Dashboard')).toBeDefined();
  });
});
