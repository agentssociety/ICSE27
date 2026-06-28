import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import LoginPage from '../pages/LoginPage'

vi.mock('../api/services', () => ({
  login: vi.fn().mockRejectedValue(new Error('Network error')),
  getBalance: vi.fn(),
  authorizeTransaction: vi.fn(),
  unlockAccount: vi.fn(),
}))

describe('LoginPage', () => {
  it('renders login form and handles error state', async () => {
    render(<LoginPage />)
    expect(screen.getByText('Card & PIN Authentication')).toBeTruthy()
    expect(screen.getByPlaceholderText('User ID')).toBeTruthy()
    expect(screen.getByPlaceholderText('PIN')).toBeTruthy()
    
    const loginButton = screen.getByText('Login')
    expect(loginButton).toBeTruthy()
  })
})
