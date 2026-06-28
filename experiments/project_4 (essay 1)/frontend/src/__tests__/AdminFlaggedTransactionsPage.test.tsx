import { describe, it, expect, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import AdminFlaggedTransactionsPage from '../pages/AdminFlaggedTransactionsPage';

vi.mock('../api/services', () => ({
  listFlaggedTransactions: vi.fn().mockResolvedValue({ data: [] }),
  reviewFlaggedTransaction: vi.fn().mockResolvedValue({}),
}));

describe('AdminFlaggedTransactionsPage', () => {
  it('renders flagged transactions heading', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <AdminFlaggedTransactionsPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Flagged Transactions')).toBeDefined();
  });
});