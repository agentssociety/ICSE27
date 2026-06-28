import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import FlaggedTransactionsPage from '../pages/FlaggedTransactionsPage'

vi.mock('../api/services', () => ({
  listAuditLogEntries: vi.fn().mockResolvedValue([
    { id: '1', userId: 'user1', eventType: 'RAPID_WITHDRAWAL', sourceIp: '10.0.0.1', outcome: 'FLAGGED' }
  ]),
  updateAuditLogEntry: vi.fn(),
}))

describe('FlaggedTransactionsPage', () => {
  it('renders flagged transactions', async () => {
    render(<FlaggedTransactionsPage />)
    await waitFor(() => {
      expect(screen.getByText('Flagged Transactions')).toBeTruthy()
    })
  })
})
