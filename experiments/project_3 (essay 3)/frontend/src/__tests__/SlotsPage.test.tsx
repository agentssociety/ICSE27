import { describe, it, expect } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import SlotsPage from '../pages/SlotsPage';

vi.mock('../api/services', () => ({
  slotApi: {
    getAll: vi.fn().mockResolvedValue([]),
    create: vi.fn().mockResolvedValue({}),
    delete: vi.fn().mockResolvedValue({}),
  },
  createStandardSlot: vi.fn().mockResolvedValue({}),
}));

vi.mock('../components/Layout', () => ({
  default: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}));

describe('SlotsPage', () => {
  it('renders the slots page with title', async () => {
    await act(async () => {
      render(
        <MemoryRouter>
          <SlotsPage />
        </MemoryRouter>
      );
    });
    expect(await screen.findByText('Slots')).toBeInTheDocument();
  });
});