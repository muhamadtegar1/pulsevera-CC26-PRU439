import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import RiskGauge from './RiskGauge'

describe('RiskGauge', () => {
  it('menampilkan persen (dibulatkan) dan label', () => {
    render(<RiskGauge score={0.3} percent={30} label="Sedang" />)
    expect(screen.getByText('30')).toBeInTheDocument()
    expect(screen.getByText('Risiko Sedang')).toBeInTheDocument()
  })

  it('fallback ke score*100 saat percent tidak diberikan', () => {
    render(<RiskGauge score={0.42} label="Tinggi" />)
    expect(screen.getByText('42')).toBeInTheDocument() // 0.42*100 dibulatkan
    expect(screen.getByText('Risiko Tinggi')).toBeInTheDocument()
  })

  it('membulatkan persen pecahan', () => {
    render(<RiskGauge score={0.156} percent={15.6} label="Rendah" />)
    expect(screen.getByText('16')).toBeInTheDocument()
  })

  it('tetap render dengan label tak dikenal (fallback warna Sedang)', () => {
    render(<RiskGauge score={0.5} percent={50} label="Unknown" />)
    expect(screen.getByText('Risiko Unknown')).toBeInTheDocument()
  })
})
