import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { act } from 'react';
import AssignUrgencyPage from '../pages/AssignUrgencyPage';
import { BrowserRouter } from 'react-router-dom';

vi.mock('../api/services', () => ({
  getPatients: vi.fn().mockResolvedValue([
    { id: 1, username: 'Alice', authentication_id: 0 },
    { id: 2, username: 'Bob', authentication_id: 0 },
  ]),
  assignUrgency: vi.fn(),
}));

describe('AssignUrgencyPage', () => {
  it('renders the assign urgency heading', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <AssignUrgencyPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByRole('heading', { level: 1, name: 'Assign Urgency Level' })).toBeTruthy();
  });

  it('shows patient options', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <AssignUrgencyPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Alice (ID: 1)')).toBeTruthy();
    expect(screen.getByText('Bob (ID: 2)')).toBeTruthy();
  });
});
