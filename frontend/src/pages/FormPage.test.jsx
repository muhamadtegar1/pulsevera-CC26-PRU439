import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

// Proxy tanpa cache membuat component type baru tiap render → React unmount/remount → input kehilangan fokus.
// Cache per tag memastikan referensi stabil sehingga React tidak mereset elemen saat re-render.
vi.mock('framer-motion', async () => {
  const React = await import('react')
  const create = React.createElement
  const strip = (p) => {
    const { initial, animate, exit, transition, whileHover, whileTap,
            variants, layout, layoutId, ...rest } = p
    return rest
  }
  const cache = {}
  const motion = new Proxy({}, {
    get: (_t, tag) => {
      if (!cache[tag]) {
        cache[tag] = React.forwardRef((props, ref) => create(tag, { ...strip(props), ref }))
      }
      return cache[tag]
    },
  })
  return { motion, AnimatePresence: ({ children }) => create(React.Fragment, null, children) }
})

import FormPage from './FormPage'

const fillStep0 = async (user) => {
  await user.click(screen.getByText('Laki-laki'))
  await user.selectOptions(screen.getByRole('combobox'), '7')
}

const clickNext = (user) => user.click(screen.getByRole('button', { name: /Lanjut/i }))

// Isi semua step sampai tepat sebelum tombol "Lihat Hasil" diklik.
const walkToSubmit = async (user) => {
  await fillStep0(user)
  await clickNext(user)

  // Step 1: Antropometri — tinggi dalam cm, berat dalam kg
  const [heightInput, weightInput] = screen.getAllByRole('spinbutton')
  await user.type(heightInput, '170')
  await user.type(weightInput, '70')
  await clickNext(user)

  // Step 2: Gaya Hidup (sleep_hours default 7 sudah valid)
  await user.click(screen.getByText('Ya, rutin'))
  await clickNext(user)

  // Step 3: Konsumsi
  await user.click(screen.getByText('Tidak pernah'))
  await user.click(screen.getByText('Tidak')) // alcohol = No
  await clickNext(user)

  // Step 4: Kondisi Kesehatan (diabetes default 'No' sudah valid)
  await user.click(screen.getByText('Baik'))
}

describe('FormPage', () => {
  it('tombol Lanjut nonaktif sampai field step valid', async () => {
    const user = userEvent.setup()
    render(<FormPage onBack={vi.fn()} onSubmit={vi.fn()} />)

    const nextBtn = screen.getByRole('button', { name: /Lanjut/i })
    expect(nextBtn).toBeDisabled()

    await fillStep0(user)
    expect(nextBtn).toBeEnabled()
  })

  it('tombol Beranda memanggil onBack di step pertama', async () => {
    const user = userEvent.setup()
    const onBack = vi.fn()
    render(<FormPage onBack={onBack} onSubmit={vi.fn()} />)

    await user.click(screen.getByRole('button', { name: /Beranda/i }))
    expect(onBack).toHaveBeenCalledTimes(1)
  })

  it('walkthrough lengkap → onSubmit dengan height_meters dalam meter (170 cm → 1.7 m)', async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn().mockResolvedValue(undefined)
    render(<FormPage onBack={vi.fn()} onSubmit={onSubmit} />)

    await walkToSubmit(user)
    await user.click(screen.getByRole('button', { name: /Lihat Hasil/i }))

    await waitFor(() => expect(onSubmit).toHaveBeenCalledTimes(1))
    const payload = onSubmit.mock.calls[0][0]

    // Input 170 cm → dikirim sebagai 1.70 meter ke API
    expect(payload.height_meters).toBeCloseTo(1.7)

    // Semua field numerik bertipe number (bukan string)
    expect(typeof payload.height_meters).toBe('number')
    expect(typeof payload.age_category).toBe('number')
    expect(typeof payload.weight_kg).toBe('number')

    expect(payload).toMatchObject({
      sex: 'Male',
      age_category: 7,
      weight_kg: 70,
      physical_activities: 'Yes',
      sleep_hours: 7,
      smoker_status: 'Never',
      alcohol: 'No',
      general_health: 'Good',
      diabetes: 'No',
    })
  })

  it('menampilkan pesan error saat onSubmit gagal', async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn().mockRejectedValue({ response: { data: { error: 'ML API down' } } })
    render(<FormPage onBack={vi.fn()} onSubmit={onSubmit} />)

    await walkToSubmit(user)
    await user.click(screen.getByRole('button', { name: /Lihat Hasil/i }))

    expect(await screen.findByText('ML API down')).toBeInTheDocument()
  })

  it('field tinggi badan: input type=number dengan min=100, max=250, step=1 (cm)', async () => {
    const user = userEvent.setup()
    render(<FormPage onBack={vi.fn()} onSubmit={vi.fn()} />)

    await fillStep0(user)
    await clickNext(user)

    const [heightInput] = screen.getAllByRole('spinbutton')
    expect(heightInput).toHaveAttribute('min', '100')
    expect(heightInput).toHaveAttribute('max', '250')
    expect(heightInput).toHaveAttribute('step', '1')
    expect(heightInput).toHaveAttribute('placeholder', '165')
    expect(screen.getByText('cm')).toBeInTheDocument()
  })

  it('BMI preview: 170 cm + 70 kg → BMI 24.2 (Ideal)', async () => {
    const user = userEvent.setup()
    render(<FormPage onBack={vi.fn()} onSubmit={vi.fn()} />)

    await fillStep0(user)
    await clickNext(user)

    const [heightInput, weightInput] = screen.getAllByRole('spinbutton')
    await user.type(heightInput, '170')
    await user.type(weightInput, '70')

    // BMI = 70 / (1.70^2) = 24.2 → kategori Ideal
    expect(await screen.findByText('24.2')).toBeInTheDocument()
    expect(screen.getByText('Ideal')).toBeInTheDocument()
  })
})
