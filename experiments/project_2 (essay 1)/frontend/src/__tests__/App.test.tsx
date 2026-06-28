import { vi } from 'vitest'
import { act, render } from '@testing-library/react'
import App from '../App'

vi.mock('../api/services', () => ({
  listBloodUnits: vi.fn().mockResolvedValue([]),
  createBloodUnit: vi.fn().mockResolvedValue({ id: 1 }),
  deleteBloodUnit: vi.fn().mockResolvedValue(undefined),
  listTransfusionRequests: vi.fn().mockResolvedValue([]),
  createTransfusionRequest: vi.fn().mockResolvedValue({ id: 1 }),
  deleteTransfusionRequest: vi.fn().mockResolvedValue(undefined),
  listReservations: vi.fn().mockResolvedValue([]),
  createReservation: vi.fn().mockResolvedValue({ id: 1 }),
  deleteReservation: vi.fn().mockResolvedValue(undefined),
  getInventoryDashboard: vi.fn().mockResolvedValue({
    stock_summary: {},
    expiring_units_count: 0,
    expiring_units: [],
    pending_requests_count: 0,
  }),
}))

describe('App', () => {
  it('renders without crashing', async () => {
    await act(async () => {
      render(<App />)
    })
  })
})
