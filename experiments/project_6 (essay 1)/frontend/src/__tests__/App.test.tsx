
import { vi } from 'vitest'
import { act, render } from '@testing-library/react'
import App from '../App'

vi.mock('../api/services', () => ({
  listPosts: vi.fn().mockResolvedValue([]),
  listUsers: vi.fn().mockResolvedValue([]),
  listNotifications: vi.fn().mockResolvedValue([]),
  listMessages: vi.fn().mockResolvedValue([]),
  listGroups: vi.fn().mockResolvedValue([]),
  listGroupMemberships: vi.fn().mockResolvedValue([]),
  listAuditLogs: vi.fn().mockResolvedValue([]),
  listUserProfiles: vi.fn().mockResolvedValue([]),
  listProfiles: vi.fn().mockResolvedValue([]),
  listNotificationPreferences: vi.fn().mockResolvedValue([]),
}))

describe('App', () => {
  it('renders without crashing', async () => {
    await act(async () => {
      render(<App />)
    })
  })
})
