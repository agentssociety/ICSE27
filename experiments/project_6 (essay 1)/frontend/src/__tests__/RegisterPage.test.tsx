
import { vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '../hooks/useAuth';
import RegisterPage from '../pages/RegisterPage';

vi.mock('../api/services', () => ({
  registerUser: vi.fn().mockResolvedValue({ userId: 1, email: 'test@test.com', message: 'Account created' }),
}));

describe('RegisterPage', () => {
  it('renders without crashing', async () => {
    await act(async () => {
      render(<BrowserRouter><AuthProvider><RegisterPage /></AuthProvider></BrowserRouter>);
    });
    expect(screen.getByText('Create Account')).toBeInTheDocument();
  });

  it('has form fields', async () => {
    await act(async () => {
      render(<BrowserRouter><AuthProvider><RegisterPage /></AuthProvider></BrowserRouter>);
    });
    expect(screen.getByPlaceholderText('Your full name')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('email@example.com')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Min 8 characters')).toBeInTheDocument();
  });
});
