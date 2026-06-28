import { vi } from 'vitest'
import { act, render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import QueuePage from '../pages/QueuePage'

vi.mock('../api/services', () => ({
  listPatients: vi.fn().mockResolvedValue([
    { id: 1, symptoms: 'Chest pain', urgencyLevel: 1, queuePosition: 1, arrivalTime: '2024-01-01T00:00:00Z', urgency: 'critical' },
    { id: 2, symptoms: 'Fever', urgencyLevel: 3, queuePosition: 2, arrivalTime: '2024-01-01T00:05:00Z', urgency: 'moderate' },
  ]),
  updatePatient: vi.fn().mockResolvedValue({}),
  deletePatient: vi.fn().mockResolvedValue({}),
}))

describe('QueuePage', () => {
  it('renders the queue sorted by urgency', async () => {
    await act(async () => {
      render(
        <MemoryRouter>
          <QueuePage />
        </MemoryRouter>
      )
    })
    expect(screen.getByText('Patient Queue')).toBeInTheDocument()
    expect(screen.getByText('Chest pain')).toBeInTheDocument()
    expect(screen.getByText('Fever')).toBeInTheDocument()
  })
})
