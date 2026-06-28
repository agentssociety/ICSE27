import { describe, it, expect, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import AdminAuditLogPage from '../pages/AdminAuditLogPage';

vi.mock('../api/services', () => ({
  listAuditLogs: vi.fn().mockResolvedValue({ data: [] }),
}));

describe('AdminAuditLogPage', () => {
  it('renders audit log heading', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <AdminAuditLogPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Audit Log')).toBeDefined();
  });
});