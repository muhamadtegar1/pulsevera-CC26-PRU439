import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3001',
  timeout: 30000,
})

/**
 * Kirim data form ke backend → ML API.
 * @param {Object} formData 10 field user
 * @returns {Promise<{risk_score, risk_percent, risk_label, top_risk_factors, recommendations, model_used, inference_ms}>}
 */
export async function predict(formData) {
  const { data } = await api.post('/api/predict', formData)
  return data
}

/**
 * Cek status backend + ML API
 */
export async function checkHealth() {
  const { data } = await api.get('/api/health')
  return data
}
