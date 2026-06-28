import { vi } from 'vitest'
import { act, render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import ReservationsPage from '../pages/ReservationsPage'

vi.mock('../api/services', () => ({
  listReservations: vi.fn().mockResolvedValue([
    { id: 1, bloodType: 'B+', quantity: 3, scheduledDate: '2026-07-01', status: 'scheduled' },
  ]),
  createReservation: vi.fn().mockResolvedValue({ id: 2, bloodType: 'O+', quantity: 1, scheduledDate: '2026-07-10', status: 'scheduled' }),
  deleteReservation: vi.fn().mockResolvedValue(undefined),
}))

describe('ReservationsPage', () => {
  it('renders reservations list', async () => {
    await act(async () => {
      render(<BrowserRouter><ReservationsPage /></BrowserRouter>)
    })
    expect(screen.getByText('Reservations')).toBeInTheDocument()
    expect(screen.getByText('New Reservation')).toBeInTheDocument()
    expect(screen.getAllByText('B+').length).toBeGreaterThan(0)
    expect(screen.getByText('scheduled')).toBeInTheDocument()
  })
})
