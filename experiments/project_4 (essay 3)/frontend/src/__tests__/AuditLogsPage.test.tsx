import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import AuditLogsPage from '../pages/AuditLogsPage';

vi.mock('../api/services', () => ({
  listAuthenticationAttempts: vi.fn().mockResolvedValue({ data: [] }),
  listTransactionLogs: vi.fn().mockResolvedValue({ data: [] }),
}));

describe('AuditLogsPage', () => {
  it('renders without crashing and shows audit logs heading', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <AuditLogsPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Audit Logs')).toBeDefined();
  });
});
