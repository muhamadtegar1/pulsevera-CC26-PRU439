const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');

const predictRoutes = require('./routes/predictRoutes');

const app = express();

app.use(helmet());
app.use(cors());
app.use(morgan('dev'));
app.use(express.json());

app.use('/api', predictRoutes);

app.get('/', (req, res) => {
  res.json({ message: 'Pulsevera API Running', service: 'pulsevera-backend' });
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'pulsevera-backend' });
});

app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint tidak ditemukan.' });
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal server error.' });
});

module.exports = app;
