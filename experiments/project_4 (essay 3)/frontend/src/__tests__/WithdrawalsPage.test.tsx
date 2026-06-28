import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import WithdrawalsPage from '../pages/WithdrawalsPage';

vi.mock('../api/services', () => ({
  listWithdrawals: vi.fn().mockResolvedValue({ data: { items: [], total: 0 } }),
  createWithdrawal: vi.fn().mockResolvedValue({}),
}));

describe('WithdrawalsPage', () => {
  it('renders without crashing and shows withdrawals heading', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <WithdrawalsPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Withdrawals')).toBeDefined();
  });
});
