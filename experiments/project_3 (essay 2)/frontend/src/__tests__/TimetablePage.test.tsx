import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import TimetablePage from '../pages/TimetablePage';

vi.mock('../api/services', () => ({
  listSlots: vi.fn().mockResolvedValue([]),
  listFlights: vi.fn().mockResolvedValue([]),
  listRunways: vi.fn().mockResolvedValue([]),
  listTimeSlots: vi.fn().mockResolvedValue([]),
}));

describe('TimetablePage', () => {
  it('renders timetable heading', async () => {
    await act(async () => {
      render(<MemoryRouter><TimetablePage /></MemoryRouter>);
    });
    expect(screen.getByText('Runway Slot Timetable')).toBeInTheDocument();
  });
});
