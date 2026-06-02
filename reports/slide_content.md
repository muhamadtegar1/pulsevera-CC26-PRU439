# Slide Presentasi — Pulsevera CC26-PRU439
> P1-2 · Struktur 10 section sesuai Mentoring 2 poin 5
> Format: [SLIDE N] Judul | Konten | Speaker Notes

---

## [SLIDE 1] COVER

**Judul:** Pulsevera  
**Subtitle:** Deteksi Dini Risiko Jantung Berbasis AI  
**Tagline:** *"Jantungmu, Cerita Masa Depanmu."*

**Visual:** Logo Pulsevera + 3D heart animation screenshot

**Badge:**
- CC26-PRU439 · DBS Foundation Coding Camp 2026
- Tim: [Nama anggota tim]

---

## [SLIDE 2] PEMBUKAAN — Mengapa Ini Penting?

**Judul:** Penyakit Jantung: Tantangan Kesehatan #1 Indonesia

**Konten (big numbers + icons):**

| 🫀 | ⚠️ | 💰 | 👥 |
|---|---|---|---|
| **635.000** kematian/tahun | **40%** serangan fatal sebelum sampai RS | **Rp 30–150 juta** per episode perawatan | **1 dari 3** penderita tidak menyadari risikonya |
| Sumber: WHO 2023 | Sumber: AHA 2024 | Sumber: BPJS 2022 | Sumber: Riskesdas 2019 |

**Highlight box:**
> "Penyakit jantung adalah *preventable* — tapi mayoritas orang tidak tahu risikonya sampai terlambat."

**Speaker notes:** Mulai dengan fakta yang mengejutkan. Angka 635.000 setara dengan kota Samarinda hilang setiap tahun. Pause sebentar setelah angka ini. Emphasize "tidak menyadari" — ini adalah gap yang Pulsevera isi.

---

## [SLIDE 3] SLIDE KHUSUS PENJURIAN — Project Overview

**Judul:** Pulsevera — Solusi Berbasis Data untuk Deteksi Dini CVD

**Konten:**

**Tech Stack:**
```
Frontend: React + Vite + Tailwind (Rifqi/Shafira)
Backend:  Express.js proxy (Rifqi)  
ML API:   FastAPI + TensorFlow (Fathan/Shafira)
Data:     CDC BRFSS 2022 · 445.132 sampel (DS Team)
```

**Checklist Main Quest:**
- ✅ Deep Learning (TF Functional API)
- ✅ Custom Component (Focal Loss + Custom Callback)
- ✅ RESTful API (Express + FastAPI)
- ✅ Networking Calls (Axios)
- ✅ Module Bundler (Vite)
- ✅ Data Wrangling, EDA, Dashboard (Streamlit)

**Checklist Side Quest:**
- ✅ FastAPI Standalone ML API
- ✅ Generative AI (Gemini)
- ✅ A/B Testing
- ✅ Feature Engineering (6 fitur baru)
- ✅ Laporan Teknis PDF

**Speaker notes:** Slide ini untuk juri yang perlu lihat checklist program. Bacakan satu per satu dengan confidence. Jika ada yang belum selesai, skip saja — fokus pada yang sudah.

---

## [SLIDE 4] PROBLEM DEFINITION

**Judul:** 3 Gap yang Membuat Risiko Jantung Tidak Terdeteksi

**Layout: 3 kolom dengan icon**

**Gap 1 — Akses Terbatas**
🏥 Screening EKG/echocardiogram memerlukan:
- Peralatan khusus (Rp 300K–2,5 juta)
- Tenaga medis spesialis
- Tidak tersedia di semua daerah

**Gap 2 — Kesadaran Rendah**
🧑 Generasi produktif (25–34 tahun) merasa:
- "Terlalu muda untuk khawatir"
- Tidak ada tools personal yang relevan
- Faktor risiko sudah terbentuk tapi tidak terasa

**Gap 3 — Tidak Ada Early Warning**
⏰ Ketika sudah terasa, sering sudah terlambat:
- 40% serangan pertama langsung fatal
- Tidak ada titik sentuh preventif yang digital

**Speaker notes:** Jangan terlalu lama di slide ini. 1 menit cukup. Emphasize bahwa semua 3 gap ini berhubungan. Gap 3 adalah AKIBAT dari gap 1 dan 2.

---

## [SLIDE 5] SOLUTION — Pulsevera

**Judul:** Pulsevera: Cek Risiko Jantung dalam 2 Menit

**Layout: Phone mockup di kanan + features di kiri**

**Cara kerja:**
1. 📝 Isi 10 pertanyaan gaya hidup (< 2 menit)
2. 🤖 AI menganalisis dengan model DL + SHAP
3. 📊 Dapatkan Skor Gaya Hidup (0–5) + Estimasi Risiko
4. 💡 Terima rekomendasi personal (Gemini AI)

**Value proposition:**
| Sebelum Pulsevera | Dengan Pulsevera |
|---|---|
| Perlu ke RS/klinik | Langsung di browser |
| Biaya Rp 300K+ | Gratis |
| 1–3 jam | < 2 menit |
| Output teknis medis | Bahasa awam + actionable |

**Disclaimer chip:** ⚠️ Bukan pengganti dokter — alat kesadaran edukasi

**Speaker notes:** Demo singkat di sini jika memungkinkan (screenshot atau video 30 detik). Emphasize "10 pertanyaan dari kehidupan sehari-hari" — bukan pertanyaan klinis yang butuh dokter.

---

## [SLIDE 6] DAMPAK — Target User & Impact

**Judul:** Untuk Siapa Pulsevera? Dan Dampaknya Apa?

**Target User (personas):**

**"Rafi" — Urban Professional 25–34**
- 👔 Kerja 8+ jam/hari, jarang olahraga
- 📱 Digital native, smartphone-first
- ❓ Tidak tahu risiko jantungnya

**"Sinta" — Keluarga Pasien CVD**
- 👨‍👩‍👧 Ada anggota keluarga pernah serangan jantung
- 🔍 Aktif mencari informasi preventif

**Impact Metrics (estimated):**

```
60 juta orang Indonesia usia 25–45
        × 0.1% adoption
= 60.000 user

60.000 × 5% terdeteksi risiko tinggi
= 3.000 potensi intervensi dini

Biaya preventif vs. emergency CVD = 10-50x lebih murah
```

**Speaker notes:** Frame ini sebagai "dampak potensial" bukan klaim. Emphasize bahwa 1 orang yang terdeteksi dini dan mengubah gaya hidup = investasi terbaik di bidang kesehatan.

---

## [SLIDE 7] DATASET & PEMILIHAN FITUR

**Judul:** Data yang Solid, Fitur yang Relevan

**Kiri — Dataset:**
**CDC BRFSS 2022**
- 🏛️ Survei resmi Centers for Disease Control & Prevention
- 📊 445.132 responden
- 40 variabel perilaku kesehatan
- Target: `HadHeartAttack` (5.6% positif)

**Kanan — Mengapa 10 Fitur ini? (SHAP validates)**

| # | Fitur Form | SHAP Rank | Medically Modifiable? |
|---|---|---|---|
| 1 | Kondisi Umum | #1 | ❌ Indicator |
| 2 | Usia | #3 | ❌ Non-modifiable |
| 3 | Diabetes | #5 | ⚠️ Manageable |
| 4 | Alkohol | #6 | ✅ Ya |
| 5 | Aktivitas Fisik | #8 | ✅ Ya |
| 6 | Tidur | #15 | ✅ Ya |
| 7 | Status Merokok | ~#20 | ✅ Ya |
| 8 | BMI (tinggi+berat) | #2 feature set | ✅ Ya |

**Footer:** *"10 field dipilih karena merupakan bagian keseharian — meminimalkan missing value"* (Mentor advice)

**Speaker notes:** Jelaskan bahwa SHAP memvalidasi pilihan fitur kami secara kuantitatif — ini bukan subjektif. Highlight bahwa fitur klinis (angina, stroke) tidak ditanyakan karena UX consideration.

---

## [SLIDE 8] BENCHMARK MODEL

**Judul:** Mengapa Deep Learning? Data Berbicara.

**Tabel benchmark:**

| Model | Accuracy | **Recall** | F1 | ROC-AUC | Train Time |
|---|---|---|---|---|---|
| Logistic Regression | 84.2% | 64.6% | 31.6% | 83.1% | 9s |
| Decision Tree | 82.8% | 62.8% | 29.2% | 81.3% | 9s |
| Random Forest | 90.9% | 44.5% | 35.6% | 84.6% | 40s |
| **DL + SMOTE (ours)** | **85.8%** | **71.2%** | **36.1%** | **88.1%** | ~300s |

**Penjelasan kenapa Recall penting:**

```
📍 Untuk medical screening:

False Negative = GAGAL DETEKSI orang yang BERISIKO
                ↑ INI BERBAHAYA

False Positive = salah flag orang yang SEHAT
               ↑ Tidak nyaman, tapi bisa diverifikasi dokter

∴ Recall > Precision untuk screening
```

**Arrow callout:** Random Forest accuracy 90.9% TAPI Recall hanya 44.5% = 56 dari 100 orang berisiko TIDAK TERDETEKSI ❌

**Speaker notes:** Ini adalah slide kunci yang akan ditanya juri. Jelaskan dengan tenang bahwa accuracy tinggi bisa "menipu" pada imbalanced dataset. RF yang accuracy-nya tinggi justru biased ke mayoritas (negatif).

---

## [SLIDE 9] MODEL FINAL & THRESHOLD TUNING

**Judul:** DL + SMOTE @ Threshold 0.23 — Sweet Spot

**Kiri — Arsitektur:**
```
Input (46 fitur)
     ↓
Dense(256, ReLU) + BatchNorm + Dropout(0.3)
     ↓
Dense(128, ReLU) + BatchNorm + Dropout(0.3)  
     ↓
Dense(64, ReLU) + BatchNorm + Dropout(0.3)
     ↓
Dense(1, Sigmoid)
     ↓
Threshold @ 0.23
     ↓
Prediksi Binary (0/1)
```

**Custom Components:**
- 🔥 **Focal Loss** (γ=2.0, α=0.25) — menghukum easy negatives
- 🛑 **EarlyStoppingByRecall** — stop saat recall tidak improve

**Kanan — Threshold Chart (fig_threshold_curves.png):**

Threshold vs Accuracy & Recall:
- Threshold 0.5: Acc 91%, Recall 30% ← terlalu bias
- **Threshold 0.23: Acc 85.76%, Recall 71.15%** ← ✅ sweet spot
- Threshold 0.1: Acc 60%, Recall 90%+ ← terlalu banyak false alarm

**Training Strategy:**
- SMOTE (sampling_strategy=0.3)
- class_weight balanced (class 1 = 2.17x)
- Focal Loss

**Final Metrics:**
| Accuracy | Recall | ROC-AUC |
|---|---|---|
| **85.76%** ✅ | **71.15%** ✅ | **88.12%** ✅ |

**Speaker notes:** Threshold 0.23 adalah hasil eksperimen dan kesepakatan tim — bukan angka sembarangan. Tunjukkan grafik threshold_curves untuk visual support.

---

## [SLIDE 10] DEMO PRODUK

**Judul:** Pulsevera — Live Demo

**Layout: Screenshots alur aplikasi**

**Screenshot 1: Landing Page**
- Tagline + CTA button
- Disclaimer "bukan pengganti dokter"

**Screenshot 2: Form (Step Antropometri)**
- 10 input form yang ramah user
- BMI auto-preview real-time
- Tooltip/helper text di setiap field

**Screenshot 3: Hasil — Lifestyle Score**
- Gauge 5/5 (utama)
- 5 checklist kebiasaan
- Grade: "Sangat Sehat" / "Berisiko"

**Screenshot 4: Hasil — Risk Score + Faktor**
- Semi-circle gauge
- 3 faktor risiko utama (SHAP-backed)
- Rekomendasi personal

**Flow narasi:**
> "User berusia 28 tahun, perokok, jarang olahraga → mengisi form 2 menit → mendapat Lifestyle Score 1/5 'Berisiko Tinggi' → rekomendasi spesifik untuk berhenti merokok dan mulai olahraga."

**Closing statement:**
> *"Pulsevera bukan tentang menakut-nakuti. Ini tentang memberi tahu — dengan data, dengan transparansi, dan dengan kepedulian."*

---

## SLIDE BONUS — Data Flow Architecture

**Judul:** Arsitektur Sistem Pulsevera

```
User Browser
    ↓ (HTTPS Request)
React Frontend (Vite + Tailwind)
    ↓ (Axios POST /api/predict)
Express.js Backend (proxy + middleware)
    ↓ (HTTP POST /predict)
FastAPI ML API
    ├── Preprocessing (46 features)
    ├── DL Model Inference (keras)
    ├── SHAP Feature Attribution
    └── Gemini AI Recommendation
    ↓ (JSON Response)
Result Page (Lifestyle Score + Risk Score + Recommendations)
```

---

## CATATAN DESAIN SLIDE

**Warna brand Pulsevera:**
- Primary: `#4F46E5` (pulse-700, indigo)
- Accent: `#10B981` (mint-500, emerald)
- Warning: `#EF4444` (coral-500, red)
- Background: Gradient putih ke biru sangat muda

**Font:** Gunakan sans-serif modern (Inter, Plus Jakarta Sans, atau Montserrat)

**Durasi presentasi:** Target 10–15 menit + 5 menit Q&A
- Slide 1–2: 1 menit
- Slide 3: 1 menit (overview)
- Slide 4–6: 3 menit (problem + solution + impact)
- Slide 7–9: 5 menit (technical — di sini biasanya banyak pertanyaan)
- Slide 10: 2 menit (demo)

**Tools:** Canva (recommended) atau Google Slides
- Template Canva: "Modern Pitch Deck" atau "Tech Startup"
- Import gambar dari `reports/` dan `notebooks/figures/`

---

*Pulsevera · CC26-PRU439 · DBS Foundation Coding Camp 2026*
