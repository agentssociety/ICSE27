import { vi } from 'vitest'
import { act, render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import RegisterPage from '../pages/RegisterPage'

vi.mock('../api/services', () => ({
  createPatient: vi.fn().mockResolvedValue({ id: 1, symptoms: 'fever', urgencyLevel: 3, arrivalTime: '2024-01-01T00:00:00Z', urgency: 'moderate', queuePosition: 0 }),
}))

describe('RegisterPage', () => {
  it('renders the registration form', async () => {
    await act(async () => {
      render(
        <MemoryRouter>
          <RegisterPage />
        </MemoryRouter>
      )
    })
    expect(screen.getByText('Register New Patient')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Describe patient symptoms...')).toBeInTheDocument()
  })
})
