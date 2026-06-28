import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import LoginPage from '../pages/LoginPage';

vi.mock('../api/services', () => ({}));

describe('LoginPage', () => {
  it('renders without crashing and shows login heading', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <LoginPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByText('Card & PIN Login')).toBeDefined();
  });
});
