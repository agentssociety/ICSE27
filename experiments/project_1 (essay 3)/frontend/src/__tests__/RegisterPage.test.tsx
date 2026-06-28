import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { act } from 'react';
import RegisterPage from '../pages/RegisterPage';
import { BrowserRouter } from 'react-router-dom';

vi.mock('../api/services', () => ({
  createPatient: vi.fn().mockResolvedValue({ id: 1, username: 'Test', authentication_id: 0 }),
  createSymptom: vi.fn().mockResolvedValue({}),
}));

describe('RegisterPage', () => {
  it('renders the registration form', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <RegisterPage />
        </BrowserRouter>
      );
    });
    expect(screen.getByRole('heading', { level: 1, name: 'Register Patient' })).toBeTruthy();
    expect(screen.getByPlaceholderText('e.g. John Doe')).toBeTruthy();
  });
});
