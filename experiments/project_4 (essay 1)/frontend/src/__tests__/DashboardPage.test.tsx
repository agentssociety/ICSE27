import { describe, it, expect, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { BrowserRouter, MemoryRouter } from 'react-router-dom';
import DashboardPage from '../pages/DashboardPage';

vi.mock('../api/services', () => ({
  getTransactionsByUser: vi.fn().mockRejectedValue(new Error('no user')),
  listTransactions: vi.fn().mockResolvedValue({ data: [] }),
  listAuditLogs: vi.fn().mockRejectedValue(new Error('no')),
  createTransaction: vi.fn().mockResolvedValue({ data: { transaction_id: '123' } }),
}));

describe('DashboardPage', () => {
  it('renders not logged in state when no user state', async () => {
    await act(async () => {
      render(
        <MemoryRouter initialEntries={['/dashboard']}>
          <DashboardPage />
        </MemoryRouter>
      );
    });
    expect(screen.getByText('Not Logged In')).toBeDefined();
  });
});