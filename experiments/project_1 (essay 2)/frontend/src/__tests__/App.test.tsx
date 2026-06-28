import { vi } from 'vitest'
import { act, render } from '@testing-library/react'
import App from '../App'

// Mock all API service calls
vi.mock('../api/services', () => ({
  listPatients: vi.fn().mockResolvedValue([]),
  getPatient: vi.fn().mockResolvedValue({}),
  createPatient: vi.fn().mockResolvedValue({}),
  updatePatient: vi.fn().mockResolvedValue({}),
  deletePatient: vi.fn().mockResolvedValue({}),
  getDashboard: vi.fn().mockResolvedValue([]),
}))

describe('App', () => {
  it('renders without crashing', async () => {
    await act(async () => {
      render(<App />)
    })
  })
})
