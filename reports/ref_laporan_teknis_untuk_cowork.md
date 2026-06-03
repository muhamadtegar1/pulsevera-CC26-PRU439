# Brief untuk Claude Cowork: Laporan Teknis PDF Komprehensif Pulsevera

> **Instruksi penggunaan:** Paste seluruh dokumen ini ke Claude Cowork sebagai konteks, lalu minta ia membuat laporan teknis PDF komprehensif berdasarkan referensi di bawah. Katakan: *"Buatkan laporan teknis PDF komprehensif untuk proyek Pulsevera berdasarkan seluruh data dan narasi di bawah ini. Gunakan format akademik yang profesional dengan cover page, daftar isi, dan section yang terstruktur."*

---

## IDENTITAS PROYEK

- **Nama proyek**: Pulsevera — Deteksi Dini Risiko Jantung Berbasis AI
- **Kode tim**: CC26-PRU439
- **Program**: Coding Camp 2026 powered by DBS Foundation
- **Tanggal**: Juni 2026
- **Tagline**: *"Jantungmu, Cerita Masa Depanmu."*

---

## STRUKTUR LAPORAN (13 Bab)

### BAB 1 — Cover & Executive Summary

**Executive Summary (tulis ringkas, ~200 kata):**
Pulsevera adalah aplikasi web berbasis AI untuk deteksi dini risiko penyakit jantung yang dikembangkan oleh tim CC26-PRU439 dalam program Coding Camp 2026 DBS Foundation. Aplikasi menganalisis 10 kebiasaan harian pengguna dan menghasilkan dua output utama: Skor Gaya Hidup (0–5) sebagai metrik primer yang actionable, dan Estimasi Risiko Serangan Jantung berbasis machine learning sebagai metrik sekunder. Model final adalah Deep Learning (TensorFlow Functional API) dengan kombinasi SMOTE + Focal Loss + threshold tuning @ 0.23, mencapai Accuracy 85.76%, Recall 71.15%, dan ROC-AUC 0.881. Aplikasi sudah di-deploy secara publik di tiga platform: ML API di Hugging Face Spaces, Backend di Hugging Face Spaces, dan Frontend di Vercel.

---

### BAB 2 — Problem Discovery

**Tulis section ini menggunakan data berikut:**

Penyakit kardiovaskular adalah pembunuh nomor 1 di Indonesia:
- 635.000 kematian/tahun (WHO Global Health Estimates 2023)
- ~17% dari seluruh kematian di Indonesia (Riskesdas 2023)
- 40% serangan pertama langsung fatal sebelum sampai RS (AHA 2024)
- Biaya perawatan per episode: Rp 30–150 juta (BPJS 2022)
- Hanya 1 dari 3 penderita faktor risiko yang mengetahui kondisinya (Riskesdas 2019)

**3 Gap yang diidentifikasi:**
1. **Akses screening terbatas**: EKG/echocardiogram perlu Rp 300K–2,5 juta, hanya di RS tipe B/C ke atas, di luar Jawa rasio dokter jantung 1:1,2 juta penduduk
2. **Kesadaran rendah usia produktif**: 68% kasus CVD fatal di usia 40–64, tapi faktor risiko mulai terbentuk usia 20-an; generasi 25–34 merasa "terlalu muda"
3. **Tidak ada early warning digital**: Tidak ada tools personal berbasis data yang spesifik dan accessible untuk masyarakat awam

---

### BAB 3 — Dataset: CDC BRFSS 2022

**Data untuk section ini:**
- **Nama**: Behavioral Risk Factor Surveillance System (BRFSS) 2022
- **Sumber**: Centers for Disease Control and Prevention (CDC), USA
- **Ukuran**: 445.132 responden
- **Target variable**: `HadHeartAttack` (binary: 0/1)
- **Class distribution**: Positif 5.64% (5.022 dari 89.027 test samples), Negatif 94.36%
- **Jumlah variabel awal**: 40+ kolom perilaku kesehatan
- **Pembagian data**: 80% train (356.105 sampel), 20% test (89.027 sampel)

**Justifikasi pemilihan dataset:**
Data Indonesia dengan kualitas yang cukup untuk supervised ML tidak tersedia publik. CDC BRFSS dipilih karena: (1) otoritas — survei resmi yang diakui WHO; (2) skala besar untuk DL yang stabil; (3) faktor risiko CVD mayor (usia, BMI, merokok, olahraga, diabetes) bersifat universal secara epidemiologis; (4) reproduksibilitas — dataset publik yang bisa diverifikasi

---

### BAB 4 — Data Wrangling

**Poin yang harus dicakup:**
- Handling missing values: imputasi median untuk numerik, modus untuk kategorik
- Encoding: binary encoding untuk ya/tidak, ordinal encoding untuk kategori berurutan (GeneralHealth: Poor=1, Fair=2, Good=3, Very Good=4, Excellent=5; AgeCategory: 1–13)
- Outlier handling: IQR method untuk BMI dan variabel kontinyu
- Train-test split: stratified 80/20 untuk menjaga proporsi kelas
- Final shape setelah wrangling: (445.132 × 46 fitur setelah engineering)

---

### BAB 5 — EDA (5 Business Questions)

**Business questions yang dijawab:**
1. Apakah aktivitas fisik berhubungan dengan risiko serangan jantung? → Ya, signifikan (p < 0.001, Mann-Whitney U)
2. Bagaimana distribusi BMI antara yang mengalami serangan jantung vs. tidak? → Penderita rata-rata BMI lebih tinggi
3. Apakah status merokok berhubungan dengan risiko jantung? → Ya, signifikan (p < 0.001, Chi-square)
4. Bagaimana pola usia terhadap risiko CVD? → Meningkat eksponensial setelah usia kategori 8 (55–59 tahun)
5. Apakah pola tidur berpengaruh? → Ya, signifikan (p < 0.05, Mann-Whitney U)

---

### BAB 6 — Feature Engineering

**6 fitur baru yang dibuat:**

| Fitur Baru | Formula | Alasan |
|---|---|---|
| `BMI` | weight(kg) / height(m)² | Standard body composition index |
| `LifestyleRiskScore` | Skor 0–5 dari 5 indikator gaya hidup | Composite lifestyle metric |
| `IsObese` | BMI ≥ 30 → 1, else 0 | Binary flag obesitas klinis |
| `IsSleepDeprived` | SleepHours < 6 → 1, else 0 | Binary flag sleep deprivation |
| `IsActiveSmoker` | SmokerStatus ∈ {Current-some, Current-every} → 1 | Binary flag perokok aktif |
| `HasChronicCondition` | diabetes OR stroke OR angina → 1 | Binary flag komorbid kronis |

**Validasi SHAP**: `LifestyleRiskScore` masuk top-20 SHAP global importance (0.011), membuktikan feature engineering menambah nilai prediktif secara kuantitatif.

---

### BAB 7 — A/B Testing

**4 hipotesis yang diuji:**

| Hipotesis | Metode | p-value | Keputusan |
|---|---|---|---|
| H1: Aktivitas fisik menurunkan risiko jantung | Mann-Whitney U | < 0.001 | Tolak H0 ✅ |
| H2: BMI tinggi meningkatkan risiko jantung | Mann-Whitney U | < 0.001 | Tolak H0 ✅ |
| H3: Status merokok meningkatkan risiko jantung | Chi-square | < 0.001 | Tolak H0 ✅ |
| H4: Tidur cukup menurunkan risiko jantung | Mann-Whitney U | < 0.05 | Tolak H0 ✅ |

Semua hipotesis terkonfirmasi → memvalidasi relevansi fitur form terhadap target variable.

---

### BAB 8 — ML Modeling: Baseline Benchmark

**Tiga model baseline:**

| Model | Accuracy | Recall (pos) | Precision (pos) | F1 (pos) | ROC-AUC | Train Time |
|---|---|---|---|---|---|---|
| Logistic Regression | 84.19% | 64.60% | 20.87% | 31.55% | 83.10% | 9.27s |
| Decision Tree | 82.83% | 62.80% | 19.03% | 29.21% | 81.26% | 9.32s |
| Random Forest | 90.91% | 44.50% | 29.63% | 35.58% | 84.61% | 40.23s |

**Observasi kritis**: Random Forest accuracy tertinggi (90.91%) TAPI Recall hanya 44.5% — artinya 56 dari 100 orang berisiko tidak terdeteksi. Tidak acceptable untuk medical screening.

---

### BAB 9 — Deep Learning: Arsitektur & Training

**Arsitektur model final:**
```
Input Layer (46 fitur)
↓
Dense(256, activation='relu', kernel_initializer='he_normal')
BatchNormalization()
Dropout(0.3)
↓
Dense(128, activation='relu', kernel_initializer='he_normal')
BatchNormalization()
Dropout(0.3)
↓
Dense(64, activation='relu', kernel_initializer='he_normal')
Dropout(0.15)
↓
Dense(1, activation='sigmoid')  → probabilitas 0–1
```

**Custom components yang diimplementasikan:**
1. **Focal Loss** (γ=2.0, α=0.25): Menghukum easy negatives lebih keras, fokus pada hard-to-classify cases. Formula: FL(p_t) = -α_t × (1-p_t)^γ × log(p_t)
2. **EarlyStoppingByRecall**: Custom Keras callback yang monitor val_recall, bukan val_loss. Stop jika recall tidak improve setelah 10 epoch; restore best weights otomatis.

**Training strategy:**
- SMOTE (sampling_strategy=0.3): oversample minority ke 30% dari majority
- class_weight balanced: class 1 = 2.167x class 0
- Optimizer: Adam (lr=1e-3)
- Batch size: 512
- Validation split: 20%
- Max epochs: 30 (early stopping aktif)

**Kenapa ReduceLROnPlateau tidak dipakai**: Menyebabkan model kolaps ke all-negative prediction saat class imbalance ekstrem — learning rate turun terlalu cepat sebelum model belajar minority class.

---

### BAB 10 — Evaluasi & Threshold Tuning

**Hasil threshold tuning:**

| Threshold | Accuracy | Recall | Precision | F1 | MAE |
|---|---|---|---|---|---|
| 0.10 | 53.77% | 93.15% | 10.28% | 18.52% | 0.462 |
| **0.23 (final)** | **85.76%** | **71.15%** | **24.14%** | **36.05%** | **0.244** |
| 0.30 | 82.01% | 68.64% | 19.27% | 30.09% | 0.180 |
| 0.50 | 90.91% | 44.50% | 29.63% | 35.58% | 0.091 |

**Threshold 0.23 dipilih karena memenuhi dua target program sekaligus**: Accuracy ≥ 85% DAN Recall ≥ 70%.

**MAE Analysis**: Target MAE ≤ 0.02 tidak dapat dicapai secara matematis untuk binary classification dengan positive rate 5.64%. Lower bound MAE = positive_rate = 0.0564. Dokumentasi lengkap di `reports/mae_analysis.md`.

**Final metrics DL+SMOTE @ threshold 0.23:**
- Accuracy: **85.76%** ✅ (target ≥ 85%)
- Recall: **71.15%** ✅ (target ≥ 70%)
- ROC-AUC: **88.12%** ✅ (kategori excellent)
- F1: 36.05% (rendah karena imbalance ekstrem — explained di laporan)

---

### BAB 11 — SHAP Interpretability

**Top 10 fitur berdasarkan SHAP global importance (TreeExplainer, sample 200):**

| Rank | Fitur | Mean |SHAP| | Tipe |
|---|---|---|---|
| 1 | GeneralHealth (Kondisi Umum) | 0.1110 | Original |
| 2 | RemovedTeeth (Gigi Dicabut) | 0.0804 | Original |
| 3 | AgeCategory (Kategori Usia) | 0.0758 | Original |
| 4 | HadAngina (Riwayat Angina) | 0.0634 | Original |
| 5 | HadDiabetes (Diabetes) | 0.0575 | Original |
| 6 | AlcoholDrinkers (Alkohol) | 0.0475 | Original |
| 7 | Race_White (Ras) | 0.0403 | Original |
| 8 | PhysicalActivities (Aktivitas) | 0.0394 | Original |
| 9 | HIVTesting | 0.0318 | Original |
| 10 | CovidPos | 0.0228 | Original |

**Engineered features dalam top-20**: LifestyleRiskScore (0.011), IsActiveSmoker, HasChronicCondition

**Justifikasi 10-field form**: Semua fitur form (sex, age, weight, height, sleep, exercise, smoking, alcohol, general health, diabetes) masuk top-20 SHAP. Fitur klinis (HadAngina, HadStroke) tidak ditanyakan karena UX consideration — user awam tidak mengetahuinya; di-default ke 0.

---

### BAB 12 — Arsitektur & Deployment

**Arsitektur sistem:**
```
User Browser (React + Vite + Tailwind)
    ↓ HTTPS / Axios POST /api/predict
Express.js Backend (proxy, CORS, middleware)
    ↓ HTTP POST /api/v1/predict
FastAPI ML API (Python)
    ├── Preprocessing (46 features)
    ├── DL Model Inference (Keras .keras)
    ├── SHAP Feature Attribution (pre-computed)
    └── Gemini AI Recommendation (gemini-2.5-flash)
    ↓ JSON Response
ResultPage (Lifestyle Score + Risk Score + Recommendations)
```

**Deployment (LIVE):**
| Service | Platform | URL |
|---|---|---|
| ML API (FastAPI + TF) | Hugging Face Spaces | https://tgrrr-pulsevera-ml-api.hf.space |
| Backend (Express.js) | Hugging Face Spaces | https://tgrrr-pulsevera-backend.hf.space |
| Frontend (React/Vite) | Vercel | https://pulsevera.vercel.app |
| Source Code | GitHub | https://github.com/muhamadtegar1/pulsevera-CC26-PRU439 |

**Performance:**
- Inference time: ~350ms per request
- Optimasi: pre-computed SHAP (dari 7000ms → 350ms)
- TF model load time: ~45 detik (cold start, sekali saja saat startup)

---

### BAB 13 — Limitations & Future Work

**Limitations:**
1. Dataset bias: CDC BRFSS adalah populasi US adults — belum divalidasi untuk populasi Indonesia
2. Class imbalance: Precision masih 24.1% — banyak false positive; user perlu memahami ini
3. 10 input saja: Fitur klinis penting (angina, stroke) tidak ditanyakan untuk UX
4. Belum ada validasi klinis oleh tenaga medis profesional
5. MAE tidak mencapai target 0.02 — constraint matematis dari binary classification dengan imbalance

**Future work:**
- Fine-tuning dengan data Indonesia (jika tersedia)
- Validasi klinis bersama fasilitas kesehatan
- Mobile app untuk akses lebih luas
- History tracking dengan consent user
- Ensemble model (XGBoost + DL)
- Integrasi dengan sistem rekam medis (ICD-10)

---

## ASET VISUAL YANG TERSEDIA (embed ke laporan)

File tersedia di folder `reports/`:
- `shap_summary_bar.png` — SHAP global importance bar chart
- `shap_summary_beeswarm.png` — SHAP beeswarm plot top-15 fitur
- `shap_dependence_generalhealth.png` — SHAP dependence plot GeneralHealth
- `dl_experiments_comparison.png` — Perbandingan 6 varian arsitektur DL
- `fig_threshold_curves.png` — Threshold vs Accuracy/Recall curve
- `fig_confusion_matrix.png` — Confusion matrix model final
- `fig_proba_distribution.png` — Distribusi probabilitas prediksi

---

## GAYA PENULISAN

- Bahasa: **Indonesia**, formal-akademik
- Tone: Objektif, berbasis data, tidak berlebihan
- Setiap klaim → sertakan angka/sumber
- Gunakan tabel untuk data komparasi
- Gunakan code block untuk arsitektur model
- Sertakan disclaimer medis di bagian deployment/evaluasi
