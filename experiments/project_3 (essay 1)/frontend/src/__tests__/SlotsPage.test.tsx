import { describe, it, expect, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

vi.mock('../api/services', () => ({
  listSlots: vi.fn().mockResolvedValue({ data: [] }),
  createSlot: vi.fn(),
}));

import SlotsPage from '../pages/SlotsPage';

describe('SlotsPage', () => {
  it('renders slot allocation page', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <SlotsPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Slot Allocation')).toBeDefined();
  });
});