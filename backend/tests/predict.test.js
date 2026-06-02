const request = require('supertest');
const axios = require('axios');

jest.mock('axios');

const app = require('../src/app');

const validBody = {
  sex: 'Male',
  age_category: 7,
  height_meters: 1.7,
  weight_kg: 70,
  sleep_hours: 7,
  physical_activities: 'Yes',
  smoker_status: 'Never',
  alcohol: 'No',
  general_health: 'Good',
};

afterEach(() => jest.clearAllMocks());

describe('POST /api/predict', () => {
  test('meneruskan body ML API saat sukses (200)', async () => {
    const mlData = { risk_score: 0.3, risk_label: 'Sedang', recommendations: ['x'] };
    axios.post.mockResolvedValue({ data: mlData });

    const res = await request(app).post('/api/predict').send(validBody);

    expect(res.status).toBe(200);
    expect(res.body).toEqual(mlData);
    expect(axios.post).toHaveBeenCalledTimes(1);
    expect(axios.post.mock.calls[0][0]).toMatch(/\/api\/v1\/predict$/);
  });

  test('400 saat field wajib hilang (tanpa memanggil ML API)', async () => {
    const { sex, ...incomplete } = validBody;

    const res = await request(app).post('/api/predict').send(incomplete);

    expect(res.status).toBe(400);
    expect(res.body.error).toMatch(/sex/);
    expect(axios.post).not.toHaveBeenCalled();
  });

  test('400 saat field bernilai string kosong', async () => {
    const res = await request(app)
      .post('/api/predict')
      .send({ ...validBody, general_health: '' });

    expect(res.status).toBe(400);
    expect(res.body.error).toMatch(/general_health/);
  });

  test('503 saat ML API tidak dapat dijangkau (ECONNREFUSED)', async () => {
    axios.post.mockRejectedValue({ code: 'ECONNREFUSED' });

    const res = await request(app).post('/api/predict').send(validBody);

    expect(res.status).toBe(503);
    expect(res.body.error).toMatch(/ML API tidak dapat dijangkau/);
  });

  test('meneruskan status & body error dari ML API (mis. 422)', async () => {
    axios.post.mockRejectedValue({
      response: { status: 422, data: { detail: 'age_category invalid' } },
    });

    const res = await request(app).post('/api/predict').send(validBody);

    expect(res.status).toBe(422);
    expect(res.body).toEqual({ detail: 'age_category invalid' });
  });

  test('500 untuk error tak terduga', async () => {
    axios.post.mockRejectedValue(new Error('boom'));

    const res = await request(app).post('/api/predict').send(validBody);

    expect(res.status).toBe(500);
    expect(res.body.error).toMatch(/Gagal mendapatkan prediksi/);
  });
});

describe('GET /api/health & 404', () => {
  test('health 200', async () => {
    const res = await request(app).get('/api/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
  });

  test('endpoint tak dikenal -> 404', async () => {
    const res = await request(app).get('/tidak-ada');
    expect(res.status).toBe(404);
    expect(res.body.error).toMatch(/tidak ditemukan/);
  });
});
