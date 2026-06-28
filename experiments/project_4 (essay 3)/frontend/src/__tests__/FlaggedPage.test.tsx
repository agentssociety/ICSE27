import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import FlaggedPage from '../pages/FlaggedPage';

vi.mock('../api/services', () => ({
  listFlaggedTransactions: vi.fn().mockResolvedValue({ data: { items: [], total: 0 } }),
  reviewFlaggedTransaction: vi.fn().mockResolvedValue({}),
}));

describe('FlaggedPage', () => {
  it('renders without crashing and shows flagged transactions heading', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <FlaggedPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Flagged Transactions')).toBeDefined();
  });
});
