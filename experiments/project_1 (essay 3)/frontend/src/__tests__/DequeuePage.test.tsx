import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { act } from 'react';
import DequeuePage from '../pages/DequeuePage';
import { BrowserRouter } from 'react-router-dom';

vi.mock('../api/services', () => ({
  dequeueNext: vi.fn(),
}));

describe('DequeuePage', () => {
  it('renders the dequeue heading', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <DequeuePage />
        </BrowserRouter>
      );
    });
    expect(screen.getByRole('heading', { level: 1, name: 'Take Next Patient' })).toBeTruthy();
  });

  it('initially shows helper text', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <DequeuePage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Click the button above to dequeue the next patient from the queue.')).toBeTruthy();
  });
});
