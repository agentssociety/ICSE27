import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import LoginPage from '../pages/LoginPage';

vi.mock('../api/services', () => ({
  loginUser: vi.fn().mockResolvedValue({ success: false, message: 'mock' }),
}));

describe('LoginPage', () => {
  it('renders the login form', async () => {
    const { container } = render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    );
    expect(screen.getByText('Card & PIN Login')).toBeDefined();
  });
});
