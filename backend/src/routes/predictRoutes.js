const express = require('express');

const {
  predictRisk,
  healthCheck,
} = require('../controllers/predictController');

const router = express.Router();

router.post('/predict', predictRisk);
router.get('/health', healthCheck);

module.exports = router;
