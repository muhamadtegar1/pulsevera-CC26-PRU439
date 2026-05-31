const axios = require('axios');

const ML_API_URL = process.env.ML_API_URL || 'http://localhost:8000';

const REQUIRED_FIELDS = [
  'sex',
  'age_category',
  'height_meters',
  'weight_kg',
  'sleep_hours',
  'physical_activities',
  'smoker_status',
  'alcohol',
  'general_health',
];

const predictRisk = async (req, res) => {
  try {
    const missing = REQUIRED_FIELDS.filter(
      (f) => req.body[f] === undefined || req.body[f] === ''
    );
    if (missing.length > 0) {
      return res.status(400).json({
        error: `Field tidak lengkap: ${missing.join(', ')}`,
      });
    }

    const mlResponse = await axios.post(
      `${ML_API_URL}/api/v1/predict`,
      req.body,
      { timeout: 15000 }
    );

    res.status(200).json(mlResponse.data);
  } catch (error) {
    if (error.response) {
      return res.status(error.response.status).json(error.response.data);
    }
    if (error.code === 'ECONNREFUSED') {
      return res.status(503).json({
        error: 'ML API tidak dapat dijangkau. Pastikan FastAPI sudah berjalan di ' + ML_API_URL,
      });
    }
    console.error('Predict error:', error.message);
    res.status(500).json({
      error: 'Gagal mendapatkan prediksi. Coba lagi.',
    });
  }
};

const healthCheck = (req, res) => {
  res.json({ status: 'ok', ml_api_url: ML_API_URL });
};

module.exports = {
  predictRisk,
  healthCheck,
};
