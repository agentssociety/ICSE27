import { vi } from 'vitest'
import { act, render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import BloodUnitsPage from '../pages/BloodUnitsPage'

vi.mock('../api/services', () => ({
  listBloodUnits: vi.fn().mockResolvedValue([
    { id: 1, bloodType: 'A', rhFactor: '+', donationDate: '2026-01-01', expirationDate: '2026-06-30', isExpiring: false },
    { id: 2, bloodType: 'O', rhFactor: '-', donationDate: '2026-05-01', expirationDate: '2026-06-15', isExpiring: true },
  ]),
  createBloodUnit: vi.fn().mockResolvedValue({ id: 3, bloodType: 'B', rhFactor: '+', donationDate: '2026-06-14', isExpiring: false }),
  deleteBloodUnit: vi.fn().mockResolvedValue(undefined),
}))

describe('BloodUnitsPage', () => {
  it('renders blood units list', async () => {
    await act(async () => {
      render(<BrowserRouter><BloodUnitsPage /></BrowserRouter>)
    })
    expect(screen.getByText('Blood Units')).toBeInTheDocument()
    expect(screen.getByText('Record New Unit')).toBeInTheDocument()
    expect(screen.getAllByText('A')[0]).toBeInTheDocument()
    expect(screen.getByText('Expiring Soon')).toBeInTheDocument()
  })
})
