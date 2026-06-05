# Pulsevera — Predict, Prevent, Prevail

**Coding Camp 2026 powered by DBS Foundation | CC26-PRU439**

> Aplikasi web prediksi risiko penyakit jantung berbasis gaya hidup menggunakan Deep Learning. Pengguna mengisi 10 pertanyaan sehari-hari dan mendapatkan estimasi risiko, skor gaya hidup, serta rekomendasi personal dari Gemini AI — dalam waktu kurang dari 2 menit.

![Tech Stack](reports/Tech%20stack.png)

---

## Daftar Isi

- [Deskripsi Proyek](#deskripsi-proyek)
- [Fitur Utama](#fitur-utama)
- [Arsitektur Sistem](#arsitektur-sistem)
- [Dataset](#dataset)
- [Instalasi & Setup](#instalasi--setup)
- [Konfigurasi](#konfigurasi)
- [Panduan Penggunaan](#panduan-penggunaan)
- [Struktur Repository](#struktur-repository)
- [Performa Model](#performa-model)
- [Kontribusi](#kontribusi)
- [Tim](#tim)
- [Lisensi & Kontak](#lisensi--kontak)

---

## Deskripsi Proyek

Pulsevera adalah platform deteksi dini risiko penyakit jantung yang dapat diakses langsung dari browser. Proyek ini dikembangkan sebagai bagian dari Capstone Project **Coding Camp 2026 powered by DBS Foundation**.

**Masalah yang diselesaikan:**
- Screening kardiovaskular konvensional memerlukan peralatan dan biaya yang tidak terjangkau semua orang
- Generasi produktif (25–34 tahun) sering tidak menyadari faktor risiko yang sudah terbentuk
- Tidak ada tools digital preventif yang ramah pengguna awam

**Solusi:**
Pulsevera menggunakan model Deep Learning yang dilatih pada data survei kesehatan 445.132 responden (CDC BRFSS 2022) untuk menghasilkan estimasi risiko berbasis kebiasaan sehari-hari, tanpa memerlukan alat medis.

---

## Fitur Utama

- **Prediksi Risiko**: Estimasi probabilitas risiko penyakit jantung dari 10 input gaya hidup
- **Skor Gaya Hidup (0–5)**: Metrik primer yang actionable untuk semua kelompok usia
- **Top Faktor Risiko**: 3 faktor dominan yang mempengaruhi hasil, didukung analisis SHAP
- **Rekomendasi Personal**: Saran kesehatan yang disesuaikan profil pengguna via Gemini AI (dengan fallback rule-based)
- **Data Insights**: Halaman visualisasi faktor risiko dari dataset populasi
- **Streamlit Dashboard**: Eksplorasi interaktif dataset CDC BRFSS 2022
- **Privacy by Design**: Tidak ada data pengguna yang disimpan — diproses real-time dan langsung dilupakan

---

## Arsitektur Sistem

```
[User Browser]
      │
      ▼
┌─────────────────────────┐
│   React Frontend        │  Vite · Tailwind CSS · Axios · Three.js
│   (Vercel / Netlify)    │
└──────────┬──────────────┘
           │ POST /api/predict
           ▼
┌─────────────────────────┐
│  Node.js / Express      │  Proxy · Rate limiting · CORS management
│  Backend (Render)       │
└──────────┬──────────────┘
           │ POST /predict
           ▼
┌─────────────────────────┐
│  FastAPI ML API         │  TensorFlow · SHAP · Gemini AI
│  (Hugging Face Spaces)  │
└──────────┬──────────────┘
           │ loads
           ▼
┌─────────────────────────┐
│  DL Model (pulsevera_   │  Dense[256→128→64] + Focal Loss
│  dl_model.keras)        │  SMOTE · Threshold @ 0.23
└─────────────────────────┘
```

---

## Dataset

Dataset **tidak disertakan di repository** karena ukurannya besar (>100MB). Download di Google Drive:

> 📁 **[Google Drive — Pulsevera Data](https://drive.google.com/drive/folders/1jtkudb-Ggt4nk9gZygS4O87hWGDT0sbH?usp=sharing)**

Setelah download, letakkan file sesuai struktur berikut:

```
data/
├── raw/dataset_raw.csv                   (445.132 baris × 40 kolom)
├── processed/dataset_cleaned.csv
└── final/
    ├── dataset_final.csv                 (+ 6 fitur engineered)
    ├── X_train.csv    (356.105 × 46)
    ├── X_test.csv     (89.027 × 46)
    ├── y_train.csv
    └── y_test.csv
```

**Sumber:** [CDC BRFSS 2022](https://www.cdc.gov/brfss/) — survei perilaku kesehatan resmi Centers for Disease Control & Prevention, 445.132 responden, target variabel `HadHeartAttack` (class imbalance: 5.6% positif).

Dokumentasi lengkap 47 kolom tersedia di [`data_dictionary.md`](data_dictionary.md).

---

## Instalasi & Setup

### Prasyarat

| Komponen | Versi Minimum |
|---|---|
| Python | 3.10+ |
| Node.js | 18+ |
| npm | 9+ |

### 1. ML API (FastAPI — Python)

```bash
cd ml-api
python -m venv .venv
.venv\Scripts\activate        # Windows
# atau: source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
cp .env.example .env           # isi GEMINI_API_KEY (opsional)
```

Untuk melatih ulang model (butuh dataset di `data/final/`):

```bash
python train.py
```

Jalankan API:

```bash
uvicorn main:app --reload --port 8000
```

Buka `http://localhost:8000/docs` untuk dokumentasi interaktif Swagger UI.

### 2. Backend (Node.js / Express)

```bash
cd backend
cp .env.example .env           # PORT=3001, ML_API_URL=http://localhost:8000
npm install
npm run dev                    # http://localhost:3001
```

### 3. Frontend (React + Vite)

```bash
cd frontend
cp .env.example .env           # VITE_API_URL=http://localhost:3001
npm install
npm run dev                    # http://localhost:5173
```

### 4. Streamlit Dashboard (opsional)

```bash
cd dashboard
pip install streamlit plotly pandas scikit-learn scipy
streamlit run app.py           # http://localhost:8501
```

### 5. Jupyter Notebooks (Data Science / AI)

```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn \
            plotly imbalanced-learn joblib tensorflow shap jupyter
jupyter notebook notebooks/
```

---

## Konfigurasi

### `ml-api/.env`

```env
# Gemini AI — opsional, ada fallback rule-based jika tidak diisi
# Dapatkan key gratis di: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=AIzaSy...

# Threshold prediksi (default: 0.23 — hasil tuning Recall/Accuracy)
PREDICTION_THRESHOLD=0.23
```

### `backend/.env`

```env
PORT=3001
ML_API_URL=http://localhost:8000
```

### `frontend/.env`

```env
VITE_API_URL=http://localhost:3001
```

---

## Panduan Penggunaan

### Alur Prediksi

1. **Buka aplikasi** di browser → klik **"Cek Risiko Sekarang"**
2. **Isi form** — 10 pertanyaan gaya hidup (tidak memerlukan alat medis):

   | Field | Keterangan |
   |---|---|
   | Jenis Kelamin | Laki-laki / Perempuan |
   | Kategori Usia | 18–24 hingga 80+ |
   | Berat & Tinggi | BMI dihitung otomatis |
   | Aktivitas Fisik | Olahraga setidaknya 30 menit/hari |
   | Jam Tidur | Rata-rata per malam |
   | Status Merokok | Tidak pernah / Mantan / Perokok aktif |
   | Konsumsi Alkohol | Ya / Tidak |
   | Kondisi Kesehatan | Penilaian subjektif kondisi umum |
   | Riwayat Diabetes | Tidak / Pre-diabetes / Ya |

3. **Lihat hasil** — dua metrik utama:
   - **Skor Gaya Hidup (0–5)**: indikator utama yang bisa diubah
   - **Estimasi Risiko**: probabilitas berbasis model DL + 3 faktor dominan
4. **Terima rekomendasi** — saran personal dari Gemini AI atau rule-based fallback

### Menjalankan Tes

```bash
# ML API
cd ml-api && pytest

# Backend
cd backend && npm test

# Frontend
cd frontend && npm test
```

---

## Struktur Repository

```
pulsevera-CC26-PRU439/
├── notebooks/                        ← Jupyter notebooks (DS + AI)
│   ├── 01_data_wrangling.ipynb       [DS] Gathering, Assessing, Cleaning
│   ├── 02_eda.ipynb                  [DS] EDA + 5 Business Questions
│   ├── 03_feature_engineering.ipynb  [DS] 6 Fitur Baru + Train-Test Split
│   ├── 04_ab_testing.ipynb           [DS] 4 Hipotesis A/B Testing
│   ├── 05_ml_modeling.ipynb          [AI] LR + RF + DT + SMOTE + Tuning
│   ├── 06_deep_learning.ipynb        [AI] TF Functional API + Focal Loss
│   ├── 07_evaluation_shap.ipynb      [AI] Evaluasi + SHAP + Threshold Tuning
│   └── figures/                      Visualisasi PNG
├── ml-api/                           FastAPI inference service
│   ├── main.py                       Endpoints + Gemini AI integration
│   ├── preprocessing.py              10 field → 46 fitur
│   ├── inference.py                  Model loading + SHAP + rekomendasi
│   ├── train.py                      Standalone training pipeline
│   ├── custom_training_gradient_tape.py  Custom tf.GradientTape loop
│   ├── dl_experiments.py             6 variasi arsitektur DL
│   ├── models/                       .keras + metadata JSON
│   ├── tensorboard_logs/             TensorBoard training logs
│   └── tests/                        pytest test suite
├── backend/                          Node.js/Express proxy
│   ├── src/
│   │   ├── app.js
│   │   ├── controllers/predictController.js
│   │   └── routes/predictRoutes.js
│   └── tests/
├── frontend/                         React + Vite + Tailwind
│   └── src/
│       ├── pages/                    Landing, Form, Result, Insights
│       ├── sections/                 Hero, Stats, Features, HowItWorks, FAQ, CTA
│       ├── components/               Navbar, Footer, RiskGauge, 3D scenes
│       └── services/api.js
├── dashboard/                        Streamlit EDA dashboard
│   └── app.py
├── reports/                          Laporan, visualisasi, & diagram
│   ├── pulsevera_comprehensive_report.pdf
│   ├── pulsevera_dl_analysis_report.pdf
│   ├── shap_summary_bar.png
│   ├── shap_summary_beeswarm.png
│   ├── dl_experiments_comparison.png
│   └── ...
├── data_dictionary.md                Dokumentasi 47 kolom dataset
└── README.md
```

---

## Performa Model

Model final: **Deep Learning + SMOTE** @ threshold 0.23

| Model | Accuracy | Recall | F1 | ROC-AUC |
|---|---|---|---|---|
| Logistic Regression | 84.2% | 64.6% | 31.6% | 83.1% |
| Decision Tree | 82.8% | 62.8% | 29.2% | 81.3% |
| Random Forest | 90.9% | 44.5% | 35.6% | 84.6% |
| **DL + SMOTE (final)** | **85.8%** | **71.2%** | **36.1%** | **88.1%** |

Recall diprioritaskan di atas accuracy karena konteks medical screening — lebih baik false positive yang bisa diverifikasi dokter daripada false negative yang terlewat. Detail analisis di [`reports/mae_analysis.md`](reports/mae_analysis.md) dan [`reports/pulsevera_dl_analysis_report.pdf`](reports/pulsevera_dl_analysis_report.pdf).

**Arsitektur DL:**
```
Input(46 fitur)
→ Dense(256, ReLU) → BatchNorm → Dropout(0.3)
→ Dense(128, ReLU) → BatchNorm → Dropout(0.3)
→ Dense(64, ReLU)  → BatchNorm → Dropout(0.3)
→ Dense(1, Sigmoid) @ threshold 0.23
```

Custom components: **Focal Loss** (γ=2.0, α=0.25) + **EarlyStoppingByRecall** callback.

---

## Kontribusi

Proyek ini dikembangkan sebagai bagian dari program pendidikan Coding Camp 2026 DBS Foundation. Untuk melaporkan bug atau memberikan saran:

1. Buka **Issues** di repository ini
2. Gunakan template yang tersedia (bug report / feature request)
3. Sertakan langkah reproduksi, environment, dan screenshot jika relevan

Pull request dipersilakan dengan catatan:
- Pastikan semua tes lulus (`pytest` / `npm test`) sebelum submit
- Ikuti konvensi kode yang sudah ada di masing-masing komponen
- Tambahkan deskripsi singkat perubahan di PR description

---

## Tim

| Nama | Role |
|---|---|
| Muh. Tegar Adyaksa | Data Scientist |
| Fathan Rasyidi Mustafa | AI Engineer |
| Shafira Kurnia Fasya | AI Engineer |
| Muhammad Rifqi Indria Nugraha | Full-Stack Web Developer |

---

## Lisensi & Kontak

Proyek ini dikembangkan untuk keperluan pendidikan dalam program **Coding Camp 2026 powered by DBS Foundation**.

**Penting:** Pulsevera adalah alat edukasi dan kesadaran — **bukan pengganti diagnosis dokter**. Hasil prediksi tidak dapat dijadikan dasar keputusan medis.

Untuk pertanyaan terkait proyek:
- **Email:** tegaradyaksa03@gmail.com
- **Repository:** [github.com/muhamadtegar1/pulsevera-CC26-PRU439](https://github.com/muhamadtegar1/pulsevera-CC26-PRU439)

---

*Dataset: CDC BRFSS 2022 · 445.132 responden · Coding Camp 2026 powered by DBS Foundation*
