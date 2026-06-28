import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { act } from 'react';

vi.mock('../api/services', () => ({
  listTransfusionRequests: vi.fn().mockResolvedValue([
    { bloodType: 'A', rhFactor: '+', quantity: 2 },
  ]),
  submitTransfusionRequest: vi.fn().mockResolvedValue({ success: true, message: 'Submitted', requestId: 'req-002' }),
}));

import TransfusionRequestsPage from '../pages/TransfusionRequestsPage';

describe('TransfusionRequestsPage', () => {
  it('renders requests list', async () => {
    await act(async () => {
      render(<TransfusionRequestsPage />);
    });
    expect(screen.getByText('Transfusion Requests')).toBeTruthy();
    expect(screen.getByText('A+ - 2 unit(s)')).toBeTruthy();
  });
});
