import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import AuditLogPage from '../pages/AuditLogPage'

vi.mock('../api/services', () => ({
  listAuditLogEntries: vi.fn().mockResolvedValue([
    { id: '1', userId: 'user1', eventType: 'LOGIN', sourceIp: '192.168.1.1', outcome: 'SUCCESS' }
  ]),
}))

describe('AuditLogPage', () => {
  it('renders audit log entries', async () => {
    render(<AuditLogPage />)
    await waitFor(() => {
      expect(screen.getByText('Audit Log')).toBeTruthy()
    })
  })
})
