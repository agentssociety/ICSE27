import { vi } from 'vitest'
import { act, render } from '@testing-library/react'
import App from '../App'

vi.mock('../api/services', () => ({
  getQueue: vi.fn().mockResolvedValue([]),
  assignUrgency: vi.fn(),
  getPatients: vi.fn().mockResolvedValue([]),
  createPatient: vi.fn(),
  createSymptom: vi.fn(),
  dequeueNext: vi.fn(),
}))

describe('App', () => {
  it('renders without crashing', async () => {
    await act(async () => {
      render(<App />)
    })
  })
})
