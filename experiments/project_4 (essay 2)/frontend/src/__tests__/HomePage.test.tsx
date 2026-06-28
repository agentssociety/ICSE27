import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import HomePage from '../pages/HomePage'

describe('HomePage', () => {
  it('renders dashboard title and feature cards', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    )
    expect(screen.getByText('Banking Security Dashboard')).toBeTruthy()
    expect(screen.getByText('Card & PIN Auth')).toBeTruthy()
    expect(screen.getByText('Audit Log')).toBeTruthy()
    expect(screen.getByText('Flagged Transactions')).toBeTruthy()
    expect(screen.getByText('Admin: Accounts')).toBeTruthy()
  })
})
