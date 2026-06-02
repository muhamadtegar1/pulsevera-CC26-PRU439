import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

// Proxy tanpa cache membuat component type baru tiap render → React unmount/remount → input kehilangan fokus.
// Cache per tag memastikan referensi stabil sehingga React tidak mereset elemen saat re-render.
vi.mock('framer-motion', async () => {
  const React = await import('react')
  const strip = (p) => {
    const { initial, animate, exit, transition, whileHover, whileTap,
            variants, layout, layoutId, ...rest } = p
    return rest
  }
  const cache = {}
  const motion = new Proxy({}, {
    get: (_t, tag) => {
      if (!cache[tag]) {
        cache[tag] = React.forwardRef((props, ref) =>
          React.createElement(tag, { ...strip(props), ref })
        )
      }
      return cache[tag]
    },
  })
  return {
    motion,
    AnimatePresence: ({ children }) => React.createElement(React.Fragment, null, children),
  }
})

// Three.js / R3F — WebGL tidak tersedia di jsdom
vi.mock('./components/three/HeartScene', () => ({ default: () => null }))
vi.mock('./components/three/MiniBlobScene', () => ({ default: () => null }))
vi.mock('@react-three/fiber', () => ({ Canvas: () => null }))
vi.mock('@react-three/drei', () => ({}))

// Networking calls di-mock
vi.mock('./services/api', () => ({
  predict: vi.fn(),
  checkHealth: vi.fn(),
}))

import App from './App'
import { predict } from './services/api'

beforeEach(() => {
  window.history.pushState({}, '', '/')
  vi.clearAllMocks()
})

describe('App — routing & integrasi', () => {
  it('menampilkan LandingPage (tombol Cek Risiko) di route /', () => {
    render(<App />)
    expect(screen.getAllByRole('button', { name: /Cek Risiko/i }).length).toBeGreaterThan(0)
  })

  it('klik CTA "Cek Risiko" membuka FormPage step 1 (Profil Dasar)', async () => {
    const user = userEvent.setup()
    render(<App />)

    await user.click(screen.getAllByRole('button', { name: /Cek Risiko/i })[0])

    await waitFor(() => {
      expect(screen.getByText('Profil Dasar')).toBeInTheDocument()
    })
  })

  it('/result tanpa router state redirect ke LandingPage', () => {
    window.history.pushState({}, '', '/result')
    render(<App />)

    expect(screen.getAllByRole('button', { name: /Cek Risiko/i }).length).toBeGreaterThan(0)
    expect(screen.queryByText('Hasil Analisis Gaya Hidup')).not.toBeInTheDocument()
  })

  it('route tak dikenal (/xyz) redirect ke LandingPage', () => {
    window.history.pushState({}, '', '/xyz')
    render(<App />)

    expect(screen.getAllByRole('button', { name: /Cek Risiko/i }).length).toBeGreaterThan(0)
  })

  it('submit form berhasil → ResultPage menampilkan grade gaya hidup', async () => {
    predict.mockResolvedValue({
      risk_score: 0.12,
      risk_percent: 12,
      risk_label: 'Rendah',
      lifestyle: {
        score: 5,
        max_score: 5,
        grade: 'Sangat Sehat',
        habits: [
          { key: 'not_smoking', label: 'Tidak merokok aktif', good: true },
          { key: 'active', label: 'Aktif berolahraga', good: true },
          { key: 'enough_sleep', label: 'Pola tidur sehat', good: true },
          { key: 'healthy_weight', label: 'BMI ideal', good: true },
          { key: 'not_drinking', label: 'Tidak konsumsi alkohol', good: true },
        ],
      },
      top_risk_factors: [{ feature: 'AgeCategory', label: 'Usia' }],
      recommendations: ['Pertahankan gaya hidup aktif Anda.'],
      recommendation_source: 'rule_based',
      model_used: 'DL+SMOTE',
      inference_ms: 48,
    })

    const user = userEvent.setup()
    render(<App />)

    // Buka form
    await user.click(screen.getAllByRole('button', { name: /Cek Risiko/i })[0])
    await waitFor(() => expect(screen.getByText('Profil Dasar')).toBeInTheDocument())

    // Step 0: Profil Dasar
    await user.click(screen.getByText('Laki-laki'))
    await user.selectOptions(screen.getByRole('combobox'), '3')
    await user.click(screen.getByRole('button', { name: /Lanjut/i }))

    // Step 1: Antropometri
    await waitFor(() => expect(screen.getByText('Antropometri')).toBeInTheDocument())
    const [heightInput, weightInput] = screen.getAllByRole('spinbutton')
    await user.type(heightInput, '165')
    await user.type(weightInput, '58')
    await user.click(screen.getByRole('button', { name: /Lanjut/i }))

    // Step 2: Gaya Hidup
    await waitFor(() => expect(screen.getByText('Gaya Hidup')).toBeInTheDocument())
    await user.click(screen.getByText('Ya, rutin'))
    await user.click(screen.getByRole('button', { name: /Lanjut/i }))

    // Step 3: Konsumsi
    await waitFor(() => expect(screen.getByText('Konsumsi')).toBeInTheDocument())
    await user.click(screen.getByText('Tidak pernah'))
    await user.click(screen.getByText('Tidak'))
    await user.click(screen.getByRole('button', { name: /Lanjut/i }))

    // Step 4: Kondisi Kesehatan → submit
    await waitFor(() => expect(screen.getByText('Kondisi Kesehatan')).toBeInTheDocument())
    await user.click(screen.getByText('Baik'))
    await user.click(screen.getByRole('button', { name: /Lihat Hasil/i }))

    // ResultPage tampil dengan grade gaya hidup
    await waitFor(() => {
      expect(screen.getByText('Gaya hidup Anda luar biasa! Pertahankan ini.')).toBeInTheDocument()
    })

    // predict() dipanggil dengan height_meters dalam meter (165 cm → 1.65 m)
    expect(predict).toHaveBeenCalledTimes(1)
    const callArg = predict.mock.calls[0][0]
    expect(callArg.height_meters).toBeCloseTo(1.65)
  })
})
