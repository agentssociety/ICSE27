import { vi } from 'vitest'
import { act, render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import DashboardPage from '../pages/DashboardPage'

vi.mock('../api/services', () => ({
  getDashboard: vi.fn().mockResolvedValue([
    { patient_id: 1, symptoms: 'Chest pain', urgency_level: 1, urgency: 'critical', queue_position: 1, estimated_wait_minutes: 5, arrival_time: '2024-01-01T00:00:00Z' },
    { patient_id: 2, symptoms: 'Fever', urgency_level: 3, urgency: 'moderate', queue_position: 2, estimated_wait_minutes: 15, arrival_time: '2024-01-01T00:05:00Z' },
  ]),
}))

describe('DashboardPage', () => {
  it('renders the dashboard with urgency and wait times', async () => {
    await act(async () => {
      render(
        <MemoryRouter>
          <DashboardPage />
        </MemoryRouter>
      )
    })
    expect(screen.getByText('Live Dashboard')).toBeInTheDocument()
    expect(screen.getByText('Chest pain')).toBeInTheDocument()
    expect(screen.getByText('5 min')).toBeInTheDocument()
    expect(screen.getByText('15 min')).toBeInTheDocument()
  })
})
