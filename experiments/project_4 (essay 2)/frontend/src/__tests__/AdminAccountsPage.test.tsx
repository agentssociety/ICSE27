import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import AdminAccountsPage from '../pages/AdminAccountsPage'

vi.mock('../api/services', () => ({
  getUser: vi.fn(),
  updateUser: vi.fn(),
  unlockAccount: vi.fn(),
}))

describe('AdminAccountsPage', () => {
  it('renders admin account management page', () => {
    render(<AdminAccountsPage />)
    expect(screen.getByText('Admin - Account Management')).toBeTruthy()
    expect(screen.getByPlaceholderText('Enter User ID')).toBeTruthy()
    expect(screen.getByText('Lookup')).toBeTruthy()
  })
})
