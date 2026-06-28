import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { act } from 'react';
import DashboardPage from '../pages/DashboardPage';
import { BrowserRouter } from 'react-router-dom';

vi.mock('../api/services', () => ({
  getQueue: vi.fn().mockResolvedValue([
    {
      patient: { id: 1, username: 'Alice', authentication_id: 0 },
      symptom: null,
      symptomRecord: undefined,
      urgency: 5,
      position: 1,
      estimatedWaitTimeMinutes: 0,
      registeredAt: new Date().toISOString(),
    },
  ]),
  assignUrgency: vi.fn(),
}));

describe('DashboardPage', () => {
  it('renders the dashboard heading', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <DashboardPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByRole('heading', { level: 1, name: 'Live Queue Dashboard' })).toBeTruthy();
  });

  it('shows patients in the queue', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <DashboardPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Alice')).toBeTruthy();
    expect(screen.getByText('5 - Critical')).toBeTruthy();
  });
});
