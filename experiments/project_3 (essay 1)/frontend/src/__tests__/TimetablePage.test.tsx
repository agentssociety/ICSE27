import { describe, it, expect, vi } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

vi.mock('../api/services', () => ({
  listRunways: vi.fn().mockResolvedValue({ data: [] }),
  getRunwayTimetable: vi.fn(),
}));

import TimetablePage from '../pages/TimetablePage';

describe('TimetablePage', () => {
  it('renders timetable page', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <TimetablePage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Runway Slot Timetable')).toBeDefined();
  });
});