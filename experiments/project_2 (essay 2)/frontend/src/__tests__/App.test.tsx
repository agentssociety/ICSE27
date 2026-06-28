import { vi } from 'vitest'
import { act, render } from '@testing-library/react'
import App from '../App'

// Mock all API service calls so tests don't make real HTTP requests in jsdom.
vi.mock('../api/services', () => ({
  listBloodUnits: vi.fn().mockResolvedValue([
    { id: 1, uniqueID: 'BLD-001', aboType: 'A', rhFactor: '+', collectionDate: '2025-01-01', expiryDate: '2025-02-12', status: 'available' },
  ]),
  listTransfusionRequests: vi.fn().mockResolvedValue([
    { bloodType: 'A', rhFactor: '+', quantity: 2 },
  ]),
  listReservations: vi.fn().mockResolvedValue([]),
  createBloodUnit: vi.fn().mockResolvedValue({}),
  deleteBloodUnit: vi.fn().mockResolvedValue(undefined),
  submitTransfusionRequest: vi.fn().mockResolvedValue({ success: true, message: 'Submitted', requestId: 'req-001' }),
  createReservation: vi.fn().mockResolvedValue({}),
  deleteReservation: vi.fn().mockResolvedValue(undefined),
}))

describe('App', () => {
  it('renders without crashing', async () => {
    await act(async () => {
      render(<App />)
    })
  })
})
