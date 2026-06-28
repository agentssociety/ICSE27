import { describe, it, expect, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import TransfusionRequestsPage from '../pages/TransfusionRequestsPage';

vi.mock('../api/services', () => ({
  listTransfusionRequests: vi.fn().mockResolvedValue([
    { id: '1', requestId: 'REQ-001', patientId: 'PAT-001', patientABORh: 'O+', bloodType: 'O+', patientID: 'PAT-001' },
  ]),
  createTransfusionRequest: vi.fn(),
  deleteTransfusionRequest: vi.fn(),
}));

describe('TransfusionRequestsPage', () => {
  it('renders the transfusion requests page with list', async () => {
    await act(async () => {
      render(
        <MemoryRouter>
          <TransfusionRequestsPage />
        </MemoryRouter>
      );
    });
    expect(screen.getByText('Transfusion Request Intake')).toBeDefined();
    expect(screen.getByText('REQ-001')).toBeDefined();
  });
});
