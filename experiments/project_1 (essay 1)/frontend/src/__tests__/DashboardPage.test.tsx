import { vi, describe, it, expect } from 'vitest'
import { act, render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import DashboardPage from '../pages/DashboardPage'

vi.mock('../api/services', () => ({
  getQueuePatients: vi.fn().mockResolvedValue([]),
}))

const wrapper = (ui: React.ReactElement) =>
  act(async () => {
    render(
      <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        {ui}
      </BrowserRouter>
    )
  })

describe('DashboardPage', () => {
  it('renders without crashing', async () => {
    await wrapper(<DashboardPage />)
  })

  it('shows the dashboard title', async () => {
    await wrapper(<DashboardPage />)
    expect(screen.getByText('Dashboard')).toBeInTheDocument()
  })
})
