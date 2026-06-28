import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import RegisterPatientPage from '../pages/RegisterPatientPage'

describe('RegisterPatientPage', () => {
  it('renders without crashing', () => {
    render(
      <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <RegisterPatientPage />
      </BrowserRouter>
    )
  })

  it('shows the register patient heading', () => {
    render(
      <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <RegisterPatientPage />
      </BrowserRouter>
    )
    expect(screen.getByRole('heading', { name: 'Register Patient' })).toBeInTheDocument()
  })
})
