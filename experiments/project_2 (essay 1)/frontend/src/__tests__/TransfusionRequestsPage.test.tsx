import { vi } from 'vitest'
import { act, render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import TransfusionRequestsPage from '../pages/TransfusionRequestsPage'

vi.mock('../api/services', () => ({
  listTransfusionRequests: vi.fn().mockResolvedValue([
    { id: 1, patientName: 'Alice', bloodType: 'A+', quantity: 2, urgency: 'urgent', status: 'pending' },
  ]),
  createTransfusionRequest: vi.fn().mockResolvedValue({ id: 2, patientName: 'Bob', bloodType: 'O-', quantity: 1, urgency: 'routine', status: 'pending' }),
  deleteTransfusionRequest: vi.fn().mockResolvedValue(undefined),
}))

describe('TransfusionRequestsPage', () => {
  it('renders transfusion requests list', async () => {
    await act(async () => {
      render(<BrowserRouter><TransfusionRequestsPage /></BrowserRouter>)
    })
    expect(screen.getByText('Transfusion Requests')).toBeInTheDocument()
    expect(screen.getByText('New Request')).toBeInTheDocument()
    expect(screen.getByText('Alice')).toBeInTheDocument()
    expect(screen.getAllByText('urgent').length).toBeGreaterThan(0)
  })
})
