import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import ResultPage from './ResultPage'

const baseResult = {
  risk_score: 0.3,
  risk_percent: 30,
  risk_label: 'Sedang',
  lifestyle: {
    score: 3,
    max_score: 5,
    grade: 'Cukup',
    habits: [
      { key: 'not_smoking', label: 'Tidak merokok aktif', good: true },
      { key: 'active', label: 'Kurang aktivitas fisik', good: false },
      { key: 'enough_sleep', label: 'Pola tidur sehat (7 jam)', good: true },
      { key: 'healthy_weight', label: 'BMI ideal (24.2)', good: true },
      { key: 'not_drinking', label: 'Konsumsi alkohol', good: false },
    ],
  },
  top_risk_factors: [
    { feature: 'AgeCategory', label: 'Usia' },
    { feature: 'BMI', label: 'Indeks Massa Tubuh (BMI)' },
    { feature: 'SmokerStatus', label: 'Status Merokok' },
  ],
  recommendations: ['Berhenti merokok sekarang.', 'Olahraga 30 menit/hari.'],
  recommendation_source: 'rule_based',
  model_used: 'MLP(test)',
  inference_ms: 12.7,
}

describe('ResultPage', () => {
  it('render null saat result kosong', () => {
    const { container } = render(<ResultPage result={null} />)
    expect(container).toBeEmptyDOMElement()
  })

  it('menampilkan grade gaya hidup, skor, dan 5 habit', () => {
    render(<ResultPage result={baseResult} />)
    expect(screen.getByText('Cukup')).toBeInTheDocument()
    expect(screen.getByText('Tidak merokok aktif')).toBeInTheDocument()
    expect(screen.getByText('Konsumsi alkohol')).toBeInTheDocument()
    // skor 3/5 di lifestyle gauge
    expect(screen.getByText('3')).toBeInTheDocument()
  })

  it('menampilkan 3 faktor risiko dengan label & feature', () => {
    render(<ResultPage result={baseResult} />)
    expect(screen.getByText('Usia')).toBeInTheDocument()
    expect(screen.getByText('Indeks Massa Tubuh (BMI)')).toBeInTheDocument()
    expect(screen.getByText('AgeCategory')).toBeInTheDocument()
  })

  it('menampilkan rekomendasi dan info model', () => {
    render(<ResultPage result={baseResult} />)
    expect(screen.getByText('Berhenti merokok sekarang.')).toBeInTheDocument()
    expect(screen.getByText('Olahraga 30 menit/hari.')).toBeInTheDocument()
    expect(screen.getByText('Model: MLP(test)')).toBeInTheDocument()
    expect(screen.getByText('Inference: 13 ms')).toBeInTheDocument() // 12.7 -> toFixed(0)
  })

  it('label sumber rekomendasi menyesuaikan gemini vs rule_based', () => {
    render(<ResultPage result={{ ...baseResult, recommendation_source: 'gemini' }} />)
    expect(screen.getByText(/Dipersonalisasi oleh AI/)).toBeInTheDocument()
  })

  it('fallback grade & risk label saat tak dikenal (tanpa crash)', () => {
    render(<ResultPage result={{ ...baseResult, lifestyle: { ...baseResult.lifestyle, grade: '???' }, risk_label: '???' }} />)
    // fallback ke meta "Cukup"/"Sedang" -> tetap render tanpa error
    expect(screen.getByText('3 Faktor Risiko Utama')).toBeInTheDocument()
  })
})
