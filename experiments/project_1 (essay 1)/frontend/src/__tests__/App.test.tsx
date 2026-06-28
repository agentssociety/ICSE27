import { vi } from 'vitest'
import { act, render } from '@testing-library/react'
import App from '../App'

vi.mock('../api/services', () => ({
  getQueuePatients: vi.fn().mockResolvedValue([]),
  dequeuePatient: vi.fn().mockResolvedValue({ patient: null, removed: false }),
}))

describe('App', () => {
  it('renders without crashing', async () => {
    await act(async () => {
      render(<App />)
    })
  })
})
