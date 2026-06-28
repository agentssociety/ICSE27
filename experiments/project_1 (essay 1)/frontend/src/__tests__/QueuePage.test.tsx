import { vi, describe, it, expect } from 'vitest'
import { act, render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import QueuePage from '../pages/QueuePage'

vi.mock('../api/services', () => ({
  getQueuePatients: vi.fn().mockResolvedValue([]),
  dequeuePatient: vi.fn().mockResolvedValue({ patient: null, removed: false }),
}))

const wrapper = (ui: React.ReactElement) =>
  act(async () => {
    render(
      <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        {ui}
      </BrowserRouter>
    )
  })

describe('QueuePage', () => {
  it('renders without crashing', async () => {
    await wrapper(<QueuePage />)
  })

  it('shows the queue management title', async () => {
    await wrapper(<QueuePage />)
    expect(screen.getByText('Queue Management')).toBeInTheDocument()
  })
})
