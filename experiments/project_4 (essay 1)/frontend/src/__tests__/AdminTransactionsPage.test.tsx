import { describe, it, expect, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import AdminTransactionsPage from '../pages/AdminTransactionsPage';

vi.mock('../api/services', () => ({
  listTransactions: vi.fn().mockResolvedValue({ data: [] }),
  listUsers: vi.fn().mockResolvedValue({ data: [] }),
  getTransactionsByUser: vi.fn().mockResolvedValue({ data: [] }),
}));

describe('AdminTransactionsPage', () => {
  it('renders transaction history heading', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <AdminTransactionsPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Transaction History')).toBeDefined();
  });
});