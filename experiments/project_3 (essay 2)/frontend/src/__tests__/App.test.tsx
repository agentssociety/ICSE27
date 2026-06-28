import { vi } from 'vitest'
import { act, render } from '@testing-library/react'
import App from '../App'

// Mock all API service calls
vi.mock('../api/services', () => ({
  listFlights: vi.fn().mockResolvedValue([]),
  listSlots: vi.fn().mockResolvedValue([]),
  listRunways: vi.fn().mockResolvedValue([]),
  listTimeSlots: vi.fn().mockResolvedValue([]),
  createFlight: vi.fn(),
  updateFlight: vi.fn(),
  deleteFlight: vi.fn(),
  createSlot: vi.fn(),
  deleteSlot: vi.fn(),
  createRunway: vi.fn(),
  updateRunway: vi.fn(),
  deleteRunway: vi.fn(),
}))

describe('App', () => {
  it('renders without crashing', async () => {
    await act(async () => {
      render(<App />)
    })
  })
})
