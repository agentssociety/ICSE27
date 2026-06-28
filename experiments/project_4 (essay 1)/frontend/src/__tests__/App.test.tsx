import { vi } from 'vitest'
import { act, render } from '@testing-library/react'
import App from '../App'

// Mock all API service calls so tests don't make real HTTP requests in jsdom.
// Add mocks for each function your service modules export.
vi.mock('../api/services', () => ({}))

describe('App', () => {
  it('renders without crashing', async () => {
    await act(async () => {
      render(<App />)
    })
  })
})
