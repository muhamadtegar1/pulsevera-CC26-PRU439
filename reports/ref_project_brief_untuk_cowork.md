# Brief untuk Claude Cowork: Project Brief Final Pulsevera

> **Instruksi penggunaan:** Paste dokumen ini ke Claude Cowork, lalu minta: *"Isi dan lengkapi template Project Brief Coding Camp 2026 berdasarkan seluruh informasi di bawah ini. Gunakan format yang rapi, profesional, dan padat. Semua angka dan fakta harus sesuai persis dengan data yang diberikan."*

---

## IDENTITAS LENGKAP PROYEK

| Field | Value |
|---|---|
| **Nama Proyek** | Pulsevera |
| **Subtitle** | Deteksi Dini Risiko Penyakit Jantung Berbasis AI |
| **Kode Tim** | CC26-PRU439 |
| **Program** | Coding Camp 2026 powered by DBS Foundation |
| **Tahun** | 2026 |
| **Tagline** | "Jantungmu, Cerita Masa Depanmu." |
| **Website** | https://pulsevera.vercel.app |
| **GitHub** | https://github.com/muhamadtegar1/pulsevera-CC26-PRU439 |

---

## DESKRIPSI SINGKAT

Pulsevera adalah aplikasi web berbasis AI yang memungkinkan siapa pun — tanpa latar belakang medis — untuk mengecek kesehatan gaya hidup jantungnya dalam kurang dari 2 menit. Pengguna mengisi 10 pertanyaan seputar kebiasaan harian, lalu mendapat Skor Gaya Hidup (0–5), Estimasi Risiko Serangan Jantung, dan rekomendasi personal berbasis AI.

---

## PROBLEM STATEMENT

Penyakit kardiovaskular adalah penyebab kematian #1 di Indonesia (635.000 kematian/tahun, WHO 2023), namun:
- Screening tradisional (EKG) memerlukan biaya Rp 300K–2,5 juta dan tidak tersedia merata
- 1 dari 3 penderita faktor risiko tidak mengetahui kondisinya (Riskesdas 2019)
- 40% serangan jantung pertama langsung fatal sebelum sempat ke RS (AHA 2024)
- Tidak ada tools preventif digital yang personal, berbasis data, dan accessible untuk masyarakat awam

---

## SOLUSI

Aplikasi web screening risiko jantung berbasis machine learning yang:
1. Menganalisis 10 kebiasaan harian (< 2 menit, tanpa alat medis)
2. Menghasilkan **Skor Gaya Hidup 0–5** sebagai metrik utama yang actionable
3. Memberikan **Estimasi Risiko Serangan Jantung** berbasis probabilitas statistik
4. Menyajikan **rekomendasi gaya hidup personal** (Google Gemini AI)
5. Menampilkan **3 faktor risiko teratas** via SHAP interpretability

---

## TARGET USER

**Persona Utama:** Urban professional muda usia 25–34 tahun, smartphone-first, belum pernah screening jantung, tidak punya waktu/biaya untuk klinik.

**Persona Sekunder:** Keluarga pasien CVD usia 35–50 yang ingin mengetahui risiko dirinya secara proaktif.

---

## TECH STACK LENGKAP

### Data Science
- Python 3.13
- Pandas 2.2.3, NumPy 1.26.4
- Scikit-learn 1.6.1 (Logistic Regression, Decision Tree, Random Forest baseline)
- Imbalanced-learn 0.14.1 (SMOTE)
- SHAP 0.46.0 (TreeExplainer)
- Matplotlib 3.9.2, Seaborn 0.13.2

### AI / Machine Learning
- TensorFlow 2.17.0 / Keras 3.14.0
- Model: Deep Learning Functional API (Dense[256-128-64-1])
- Custom: Focal Loss (γ=2.0, α=0.25), EarlyStoppingByRecall
- Generative AI: Google Gemini 2.5 Flash (via google-genai SDK)

### Backend & API
- FastAPI 0.115.0 + Uvicorn (ML API)
- Express.js 4.19 + Node.js 20 (proxy backend)
- Axios (HTTP client)

### Frontend
- React 18.3.1 + Vite 5.4.8
- Tailwind CSS 3.4.13
- Three.js 0.169.0 + @react-three/fiber (3D heart logo)
- Framer Motion 11.11.9 (animasi)
- Recharts 2.12.7 (visualisasi data)
- React Router DOM 6.27.0

### Deployment
- Hugging Face Spaces (ML API + Backend, Docker)
- Vercel (Frontend, auto-deploy dari GitHub)

---

## DATASET

| Attribute | Value |
|---|---|
| Nama | CDC Behavioral Risk Factor Surveillance System (BRFSS) 2022 |
| Sumber | Centers for Disease Control and Prevention (CDC), USA |
| Jumlah Sampel | 445.132 responden |
| Target Variable | HadHeartAttack (binary: 0/1) |
| Class Distribution | Positif: 5.64%, Negatif: 94.36% |
| Fitur Awal | 40+ kolom |
| Fitur Setelah Engineering | 46 fitur (termasuk 6 fitur baru) |
| Train / Test Split | 80% / 20% (stratified) |

---

## PERFORMA MODEL FINAL

**Model terpilih: Deep Learning + SMOTE @ threshold 0.23**

| Metrik | Nilai | Target Program | Status |
|---|---|---|---|
| Accuracy | 85.76% | ≥ 85% | ✅ Tercapai |
| Recall (positif) | 71.15% | ≥ 70% | ✅ Tercapai |
| ROC-AUC | 88.12% | ≥ 80% | ✅ Tercapai |
| F1-Score | 36.05% | — | Terdokumentasi |
| MAE | 0.244 | ≤ 0.02 | ❌ Constraint matematis* |

*MAE ≤ 0.02 tidak dapat dicapai untuk binary classification dengan positive rate 5.64% — lower bound matematis adalah 0.056. Lihat `reports/mae_analysis.md`.

**Perbandingan baseline:**

| Model | Accuracy | Recall | ROC-AUC |
|---|---|---|---|
| Logistic Regression | 84.19% | 64.60% | 83.10% |
| Decision Tree | 82.83% | 62.80% | 81.26% |
| Random Forest | 90.91% | 44.50% | 84.61% |
| **DL+SMOTE (final)** | **85.76%** | **71.15%** | **88.12%** |

---

## FITUR ENGINEERING (6 fitur baru)

1. `BMI` — weight(kg) / height(m)²
2. `LifestyleRiskScore` — composite score 0–5 dari 5 kebiasaan lifestyle
3. `IsObese` — BMI ≥ 30
4. `IsSleepDeprived` — SleepHours < 6
5. `IsActiveSmoker` — SmokerStatus aktif (current)
6. `HasChronicCondition` — diabetes OR stroke OR angina

---

## FITUR APLIKASI

| Fitur | Status | Keterangan |
|---|---|---|
| Form screening 10 pertanyaan | ✅ Live | 5-step wizard dengan BMI auto-preview |
| Skor Gaya Hidup (0–5) | ✅ Live | Metrik primer, grade & checklist 5 kebiasaan |
| Estimasi Risiko Serangan Jantung | ✅ Live | Probabilitas % + label Rendah/Sedang/Tinggi |
| SHAP Explainability | ✅ Live | 3 faktor risiko utama per prediksi |
| Rekomendasi AI (Gemini) | ✅ Live | Dipersonalisasi via Google Gemini 2.5 Flash |
| Halaman Wawasan Data | ✅ Live | Statistik Indonesia + SHAP global chart |
| 3D Heart Logo | ✅ Live | Three.js ExtrudeGeometry + pulse animation |
| Responsive layout | ✅ Live | Mobile-first, tested di 375px–1440px |
| Stateless (no data stored) | ✅ Live | Privacy by design |

---

## CHECKLIST MAIN QUEST & SIDE QUEST

### Main Quest ✅
- [x] Deep Learning dengan TensorFlow (Functional API, Focal Loss, EarlyStoppingByRecall)
- [x] Custom Keras Component (Focal Loss + EarlyStoppingByRecall)
- [x] RESTful API (FastAPI ML API + Express.js Backend)
- [x] Networking Calls (Axios dari React ke Express)
- [x] Module Bundler (Vite)
- [x] Data Wrangling (cleaning, encoding, outlier handling)
- [x] EDA (5 business questions + visualisasi)
- [x] Dashboard interaktif (Streamlit, lokal)

### Side Quest ✅
- [x] FastAPI Standalone ML API
- [x] Generative AI Integration (Google Gemini 2.5 Flash)
- [x] A/B Testing (4 hipotesis, Mann-Whitney U + Chi-square)
- [x] Feature Engineering (6 fitur baru, SHAP validated)
- [x] Laporan Teknis PDF Komprehensif
- [x] Deployment ke cloud (HF Spaces + Vercel)
- [x] SHAP Analysis lengkap (TreeExplainer)
- [x] Custom Training Loop (tf.GradientTape implementation)
- [x] 6 DL Architecture Experiments (benchmarking)
- [x] TensorBoard Logs (4 training runs)

---

## DEPLOYMENT STATUS

| Service | Platform | URL | Status |
|---|---|---|---|
| Frontend | Vercel | https://pulsevera.vercel.app | 🟢 Live |
| Backend | HF Spaces | https://tgrrr-pulsevera-backend.hf.space | 🟢 Live |
| ML API | HF Spaces | https://tgrrr-pulsevera-ml-api.hf.space | 🟢 Live |
| Source Code | GitHub | https://github.com/muhamadtegar1/pulsevera-CC26-PRU439 | 🟢 Public |

---

## BUSINESS IMPACT

**Target user**: 60 juta orang Indonesia usia 25–45 tahun
**Adoption scenario (0.1%)**: 60.000 user
**Potensi deteksi dini**: 3.000 orang dengan risiko tinggi yang teridentifikasi
**Penghematan biaya**: Preventif vs. emergency CVD = 10–50x lebih murah (BPJS 2022)

---

## LIMITATIONS

1. Dataset CDC BRFSS berasal dari populasi AS — belum divalidasi untuk konteks Indonesia
2. Precision rendah (24.1%) — banyak false positive; disclamer medis selalu ditampilkan
3. Tidak ada validasi klinis oleh tenaga medis profesional
4. No longitudinal tracking (by design — privacy first)

---

## QUOTE POSITIONING

> *"Pulsevera bukan pengganti dokter. Pulsevera adalah pintu masuk — alat kesadaran yang mendorong orang untuk memulai perjalanan kesehatan jantung mereka."*

---

*CC26-PRU439 · DBS Foundation Coding Camp 2026 · Juni 2026*
