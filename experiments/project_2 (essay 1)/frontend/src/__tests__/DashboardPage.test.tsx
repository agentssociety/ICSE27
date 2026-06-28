import { vi } from 'vitest'
import { act, render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import DashboardPage from '../pages/DashboardPage'

vi.mock('../api/services', () => ({
  getInventoryDashboard: vi.fn().mockResolvedValue({
    stock_summary: { 'A+': 5, 'O-': 3 },
    expiring_units_count: 1,
    expiring_units: [{ id: 1, bloodType: 'A+', rhFactor: '+', expirationDate: '2026-06-20' }],
    pending_requests_count: 2,
  }),
}))

describe('DashboardPage', () => {
  it('renders inventory dashboard with stock and expiring units', async () => {
    await act(async () => {
      render(
        <BrowserRouter>
          <DashboardPage />
        </BrowserRouter>
      )
    })
    expect(screen.getByText('Inventory Dashboard')).toBeInTheDocument()
    expect(screen.getByText('Blood Types in Stock')).toBeInTheDocument()
    expect(screen.getByText('Expiring Soon')).toBeInTheDocument()
    expect(screen.getByText('Pending Requests')).toBeInTheDocument()
    expect(screen.getAllByText('A+').length).toBeGreaterThan(0)
  })
})
