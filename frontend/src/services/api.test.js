import { describe, it, expect, vi, beforeEach } from 'vitest'

// vi.hoisted() memastikan post/get terinisialisasi sebelum vi.mock factory dijalankan
const { post, get } = vi.hoisted(() => ({
  post: vi.fn(),
  get: vi.fn(),
}))

vi.mock('axios', () => ({
  default: { create: () => ({ post, get }) },
}))

import { predict, checkHealth } from './api'

beforeEach(() => {
  post.mockReset()
  get.mockReset()
})

describe('services/api', () => {
  it('predict() POST ke /api/predict dan mengembalikan data', async () => {
    const payload = { sex: 'Male', age_category: 7 }
    post.mockResolvedValue({ data: { risk_label: 'Sedang' } })

    const result = await predict(payload)

    expect(post).toHaveBeenCalledWith('/api/predict', payload)
    expect(result).toEqual({ risk_label: 'Sedang' })
  })

  it('checkHealth() GET ke /api/health', async () => {
    get.mockResolvedValue({ data: { status: 'ok' } })

    const result = await checkHealth()

    expect(get).toHaveBeenCalledWith('/api/health')
    expect(result).toEqual({ status: 'ok' })
  })

  it('predict() meneruskan error dari axios', async () => {
    post.mockRejectedValue(new Error('network down'))
    await expect(predict({})).rejects.toThrow('network down')
  })

  it('predict() mengirim payload lengkap dengan height_meters dalam meter', async () => {
    const payload = {
      sex: 'Female',
      age_category: 3,
      height_meters: 1.65,
      weight_kg: 58,
      physical_activities: 'Yes',
      sleep_hours: 8,
      smoker_status: 'Never',
      alcohol: 'No',
      general_health: 'Good',
      diabetes: 'No',
    }
    post.mockResolvedValue({ data: { risk_score: 0.1, risk_label: 'Rendah' } })

    const result = await predict(payload)

    expect(post).toHaveBeenCalledWith('/api/predict', payload)
    expect(result.risk_label).toBe('Rendah')
  })
})
