# Pulsevera ML API

FastAPI service untuk inferensi risiko penyakit jantung — bagian dari proyek **Pulsevera (CC26-PRU439)**, Coding Camp 2026 powered by DBS Foundation.

Owner: **AI Engineer** — Fathan Rasyidi Mustafa & Shafira Kurnia Fasya.

---

## Arsitektur

```
[ Web Form 10 field ]
        │
        ▼  HTTP POST /api/predict
[ Backend Node.js/Express ]
        │
        ▼  HTTP POST /api/v1/predict
[ FastAPI (ml-api) ]
        │   1. preprocessing.py  — 10 field → 46 fitur
        │   2. inference.py      — predict + SHAP + recommendations
        ▼
[ pulsevera_ml_model.pkl / pulsevera_dl_model.keras ]
```

---

## Struktur Folder

```
ml-api/
├── main.py                ← FastAPI app (entry point)
├── preprocessing.py       ← 10-field → 46-feature pipeline
├── inference.py           ← Model loading, SHAP, recommendations
├── train.py               ← Standalone training pipeline
├── requirements.txt
├── models/                ← Hasil training (di-gitignore)
│   ├── pulsevera_ml_model.pkl
│   ├── pulsevera_dl_model.keras
│   ├── scaler.pkl
│   ├── shap_explainer.pkl
│   ├── feature_metadata.json
│   ├── dl_metadata.json
│   ├── ml_results.json
│   └── shap_metadata.json
└── tensorboard_logs/      ← TensorBoard runs
```

---

## Setup

```bash
cd ml-api
python -m venv .venv
.venv\Scripts\activate          # Windows PowerShell
# source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
```

> **Catatan TensorFlow di Windows:** Mulai TF 2.11 dukungan GPU resmi di Windows hanya via WSL2. Untuk training cepat tanpa GPU, kurangi epoch (`python train.py --epochs 15`) atau pakai Google Colab.

---

## Cara Pakai

### 1. Download dataset

Lihat root `README.md`. Letakkan di:
```
pulsevera-cc26-pru439/data/final/
    ├── X_train.csv
    ├── X_test.csv
    ├── y_train.csv
    └── y_test.csv
```

### 2. Latih semua model

```bash
cd ml-api
python train.py                      # full (ML + DL + tuning + SHAP)
python train.py --no-tune            # skip hyperparameter search
python train.py --skip-dl            # ML only (cepat, ringan)
python train.py --skip-shap          # skip explainer serialization
python train.py --epochs 15          # batasi epoch DL
```

Output ke `ml-api/models/` (di-gitignore).

### 3. Setup .env (untuk Gemini AI recommendations)

```bash
cp .env.example .env
# Edit .env dan isi GEMINI_API_KEY dengan API key Gemini Anda
```

Isi `.env`:
```env
GEMINI_API_KEY=PASTE_YOUR_GEMINI_API_KEY_HERE
GEMINI_MODEL=gemini-2.5-flash
GEMINI_FALLBACK_MODELS=gemini-2.0-flash
GEMINI_ENABLED=true
```

> Jika `GEMINI_API_KEY` belum diisi / `google-genai` belum terpasang / semua model Gemini gagal, API otomatis memakai **fallback rule-based** dari `inference.generate_recommendations()`. Endpoint tetap berjalan normal.

### 4. Jalankan API

```bash
uvicorn main:app --reload --port 8000
```

Dokumentasi otomatis tersedia di:
- Swagger UI : `http://localhost:8000/docs`
- ReDoc      : `http://localhost:8000/redoc`

---

## Endpoints

| Method | Path | Deskripsi |
|---|---|---|
| `GET` | `/` | Info API |
| `GET` | `/health` | Liveness & status model |
| `GET` | `/api/v1/metadata` | Metadata model + metrik + SHAP top factors |
| `POST` | `/api/v1/predict` | Prediksi via ML (default) |
| `POST` | `/api/v1/predict-dl` | Prediksi via Deep Learning |

### Contoh Request

```bash
curl -X POST http://localhost:8000/api/v1/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"sex\":\"Male\",\"age_category\":10,\"height_meters\":1.72,\"weight_kg\":92,\"sleep_hours\":5.5,\"physical_activities\":\"No\",\"smoker_status\":\"Current-every\",\"alcohol\":\"Yes\",\"general_health\":\"Fair\",\"diabetes\":\"Yes\"}"
```

### Contoh Response

```json
{
  "risk_score": 0.7218,
  "risk_percent": 72.18,
  "risk_label": "Tinggi",
  "top_risk_factors": [
    {"feature": "AgeCategory",        "label": "Usia"},
    {"feature": "SmokerStatus",       "label": "Status Merokok"},
    {"feature": "LifestyleRiskScore", "label": "Skor Gaya Hidup"}
  ],
  "recommendations": [
    "Usia adalah faktor risiko yang tidak bisa diubah — kompensasi dengan check-up jantung tahunan dan gaya hidup sehat.",
    "Berhenti merokok — risiko serangan jantung turun signifikan dalam 1 tahun setelah berhenti.",
    "Skor gaya hidup berisiko. Mulai dari satu kebiasaan kecil (mis. jalan kaki 20 menit/hari) lalu tambah perlahan."
  ],
  "recommendation_source": "gemini",
  "model_used": "Random Forest (tuned)",
  "inference_ms": 23.41
}
```

> Field `recommendation_source` bernilai `"gemini"` bila Gemini AI aktif & berhasil, atau `"rule_based"` bila fallback dipakai.

---

## Input Mapping (10 Field Web Form)

| Field | Tipe | Nilai yang Diterima |
|---|---|---|
| `sex` | string | `Male` / `Female` |
| `age_category` | int 1..13 | 1=18-24, 2=25-29, … 13=80+ |
| `height_meters` | float | 1.0–2.5 |
| `weight_kg` | float | 30–200 |
| `sleep_hours` | float | 1–14 |
| `physical_activities` | string | `Yes` / `No` |
| `smoker_status` | string | `Never` / `Former` / `Current-some` / `Current-every` |
| `alcohol` | string | `Yes` / `No` |
| `general_health` | string | `Poor` / `Fair` / `Good` / `Very good` / `Excellent` |
| `diabetes` | string (opt) | `No` / `Pre-diabetes` / `Yes` (default `No`) |

> 36 fitur lain (riwayat penyakit detail, disabilitas, vaksinasi, ras, dll) diisi default berdasarkan distribusi populasi training — lihat `preprocessing.py:DEFAULT_VALUES`.

---

## Custom Components AI (Coding Camp checklist)

| Komponen | Implementasi |
|---|---|
| TensorFlow Functional API | `build_heart_disease_model()` di `train.py` & notebook 06 |
| Custom Loss | `focal_loss` (gamma=2.0, alpha=0.25) — atasi class imbalance ~5.6% |
| Custom Callback | `EarlyStoppingByRecall` — stop bila val_recall stagnan |
| Hyperparameter Tuning | `RandomizedSearchCV(scoring='f1')` di train.py |
| SHAP Interpretability | `TreeExplainer` / `LinearExplainer` di `inference.py` |
| Model produksi | `.keras` (DL) + `.pkl` (ML) |

---

## TensorBoard

```bash
tensorboard --logdir ml-api/tensorboard_logs
```

Buka `http://localhost:6006` untuk melihat kurva training.

---

## Deployment

Sederhana di Render / Railway:

```yaml
# render.yaml (contoh)
services:
  - type: web
    name: pulsevera-ml-api
    env: python
    plan: starter
    buildCommand: pip install -r ml-api/requirements.txt
    startCommand: cd ml-api && uvicorn main:app --host 0.0.0.0 --port $PORT
```

> Model `.pkl` + `.keras` ukurannya bisa >100 MB — pertimbangkan menyimpan di S3 / Hugging Face dan download saat startup, atau gunakan Git LFS.

---

## Troubleshooting

| Masalah | Solusi |
|---|---|
| `Model belum dilatih` di `/health` | Jalankan `python train.py` (butuh data di `data/final/`) |
| `data/final/ tidak ditemukan` | Download dataset (lihat root README) |
| `ImportError: tensorflow` | `pip install tensorflow==2.17.0` (Python 3.10–3.12) |
| Prediksi DL beda dari ML | Threshold DL ada di `dl_metadata.json:best_threshold` |
| OOM saat tuning RF | Tambahkan `--no-tune` atau kurangi `n_iter` di `train.py:train_ml()` |

---

*Pulsevera CC26-PRU439 — Coding Camp 2026 powered by DBS Foundation.*
