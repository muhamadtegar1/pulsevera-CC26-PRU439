# Pulsevera — TODO Final

> **Panduan eksekusi akhir capstone CC26-PRU439**
> Disusun dari merger 2 dokumen panduan: `Mentoring.txt` (saran 2 sesi mentor) + `Worksheet Captone.pdf` (official checklist program).
> Hanya berisi tugas yang **belum** dikerjakan, diurutkan berdasarkan urgensi.

---

## 🚨 P0 — BLOCKER (Wajib sebelum submission)

> Item Main Quest yang **harus** verified, tanpa ini submission tidak valid.

### P0-1. Browser test end-to-end — verify fitur tidak crash
- **Source**: Worksheet Captone, Main Quest Front-End ("memastikan fitur utama tidak crash")
- **Status saat ini**: Code ready, smoke test API ✅, tapi browser belum di-test runtime
- **Yang dilakukan**:
  - Buka http://localhost:5173 di browser
  - Klik full flow: Landing → Form (5 step) → Result
  - Test 3 profil: usia muda sehat, usia muda buruk, usia tua chronic
  - Verify: navigation, validation, loading state, result rendering, mobile responsive
- **Effort**: ~30 menit
- **Owner**: Anda (perlu interaksi browser)

---

## 🔴 P1 — HIGH URGENCY (Deliverable submission utama)

> Item yang harus ada untuk **demo & presentasi penjuri**.

### P1-1. Laporan Teknis PDF Komprehensif
- **Source**: Worksheet Captone DS Side Quest — "laporan teknis komprehensif dari Problem Discovery hingga hasil akhir"
- **Status saat ini**: Ada `reports/pulsevera_dl_analysis_report.pdf` tapi scope terbatas ke validasi threshold
- **Yang dilakukan**: Bikin laporan end-to-end mencakup:
  1. Cover + Executive Summary
  2. Problem Discovery: penyakit jantung di Indonesia, target user
  3. Dataset: CDC BRFSS 2022, justifikasi pemilihan
  4. Data Wrangling: cleaning, encoding, outlier handling
  5. EDA: 5 business questions + visualisasi
  6. Feature Engineering: 6 fitur baru + justifikasi
  7. A/B Testing: 4 hipotesis + hasil
  8. ML Modeling: 3 baseline + benchmark
  9. Deep Learning: arsitektur, Focal Loss, training
  10. Evaluation: threshold tuning, sweet spot @ 0.23
  11. SHAP Interpretability: top features + interpretasi
  12. Architecture & Deployment: ML API + Backend + Frontend
  13. Limitations & Future Work
- **Effort**: 3-4 jam (sebagian besar dari notebooks + analysis report yang sudah ada)
- **Owner**: Anda dengan generator script otomatis

### P1-2. Slide Presentasi Final
- **Source**: Mentor Notes poin 5 — struktur ketat dari mentor
- **Status saat ini**: Belum ada slide
- **Struktur (sesuai mentor)**:
  1. Judul
  2. Pembukaan (statistik penyakit jantung Indonesia)
  3. Slide khusus penjurian (overview project)
  4. Problem Definition
  5. Solution (Pulsevera)
  6. Dampak (target user, impact metric)
  7. Penjelasan Dataset + Alasan Pemilihan Fitur (pakai SHAP)
  8. Perbandingan Benchmark Model (ML vs DL, dengan tabel Acc/Recall/F1/ROC-AUC)
  9. Pemilihan Model Akhir (DL+SMOTE @ thr 0.23)
  10. Demo Produk (screenshot/video flow)
- **Effort**: 2-3 jam outline content + 1-2 jam visual di Canva/Google Slides
- **Owner**: Anda

### P1-3. Q&A Document untuk Penjurian
- **Source**: Mentor Notes poin 6
- **Status saat ini**: Belum ada
- **Yang dilakukan**: Compile 15-20 expected questions + jawaban siap pakai:
  - Justifikasi pemilihan dataset (CDC BRFSS authority, 445K samples, public)
  - Pendekatan handling class imbalance (SMOTE + class_weight + Focal Loss + threshold tuning)
  - Relevansi fitur ke real-life user (10 field keseharian)
  - Trade-off precision vs recall untuk medical screening
  - Kenapa Recall lebih penting daripada Accuracy
  - Kenapa DL > ML untuk produksi
  - Mengapa user muda dapat "Rendah" tapi Lifestyle bisa "Berisiko"
- **Effort**: 1-1.5 jam
- **Owner**: Anda + tim

### P1-4. Business Narrative & Impact Statement
- **Source**: Mentor Notes poin 7 — "fokus business process & impact, bukan murni teknis"
- **Status saat ini**: Belum ada articulated narrative
- **Yang dilakukan**:
  - Riset statistik penyakit jantung Indonesia (Kemenkes, WHO data)
  - Problem statement (akses screening, kesadaran preventif)
  - Target user persona (orang awam 25-34)
  - Impact metric (jumlah user screened, high-risk flagged)
  - Value proposition (early awareness > diagnosis)
- **Effort**: 1-1.5 jam
- **Owner**: Anda

### P1-5. Aktivasi Gemini API + Loading Indicator + Konsistensi ✅
- **Source**: Worksheet AI Side Quest + Mentoring 1 #1 + #8
- **Status saat ini**: ✅ `.env` dibuat dari `.env.example` (isi GEMINI_API_KEY untuk aktifkan). Loading indicator multi-step cycling ditambahkan. Gemini prompt diperbarui dengan risk_label + lifestyle_grade untuk konsistensi tone.
- **Mengapa P1**: 200+ lines code investment dormant. Untuk demo penjuri, rekomendasi Gemini-generated jauh lebih impactful.
- **Yang dilakukan**:
  1. **Aktivasi** (~10 menit):
     - Get API key di Google AI Studio (gratis): https://aistudio.google.com/app/apikey
     - Buat `ml-api/.env` dari `.env.example`, isi `GEMINI_API_KEY=AIzaSy...`
     - Restart ml-api → cek `/health` → `gemini_recommendations: true`
     - Test prediksi → `recommendation_source` harus `"gemini"`
  2. **Loading indicator** (~30 menit) — Mentoring 1 #1:
     - Tambah pesan loading di FormPage submit & ResultPage: "Sedang menyiapkan rekomendasi kesehatan personal..."
     - Animation/spinner saat tunggu Gemini response (~1-3 detik)
  3. **Konsistensi check** (~30 menit) — Mentoring 1 #8:
     - Test 4 skenario: user sehat (Lifestyle 5/5, Risk Rendah), user buruk (Lifestyle 0/5, Risk Tinggi), edge cases (medium-medium, low-high)
     - Verify Gemini recommendations tidak contradict label (mis. user "Rendah" tidak dapat rekomendasi "konsultasi darurat")
     - Refine prompt kalau perlu
- **Effort**: ~1-1.5 jam total (10 menit setup + 30 menit UI + 30 menit testing)
- **Owner**: Anda

### P1-6. Halaman Visualisasi Data Insight di Web App ✅
- **Source**: Mentoring 1 #2 + #3
- **Status saat ini**: ✅ InsightsPage.jsx dibuat di route /insights. Navbar LandingPage ditambahkan link "Wawasan Data". Aplikasi saat ini hanya Home → Prediksi. Visualisasi data ada di Streamlit dashboard terpisah (port 8501)
- **Mengapa P1**: Mentor explicitly minta struktur aplikasi "Home → Prediksi → Visualisasi Data". Tujuan: educational value untuk user awam, showcase data yang tidak masuk ke 10 field input.
- **Yang dilakukan**:
  1. Tambah route `/insights` di react-router (App.jsx)
  2. Buat `InsightsPage.jsx` dengan section:
     - **Statistik penyakit jantung Indonesia** (chart sederhana, support business narrative)
     - **Top risk factors di populasi global** (dari SHAP global importance — `shap_metadata.json`)
     - **Insight fitur clinical yang tidak ditanyakan ke user** (Angina, Stroke, COPD, dll) — sesuai mentor poin #3:
       > "Faktor ini juga berpengaruh terhadap risiko jantung. Disarankan konsultasi lebih lanjut ke dokter."
     - Optional: Link ke Streamlit dashboard untuk explore lebih dalam
  3. Update Navbar: tambah link "Insights" di nav items
- **Effort**: 2-3 jam
- **Owner**: Anda (atau Rifqi/Shafira sebagai Full-Stack)

---

## 🟡 P2 — MEDIUM URGENCY (Side quest valuable)

> Item yang menambah nilai signifikan, tapi tidak block submission.

### P2-1. Deployment Aplikasi Web (Frontend + Backend + ML-API)
- **Source**: Worksheet Front-End Side Quest — "deployment aplikasi web ke server"
- **Status saat ini**: Cuma jalan lokal
- **Yang dilakukan**:
  - **ML API**: Hugging Face Spaces (FastAPI + TF support, free)
  - **Backend**: Railway / Render (free tier 750h/bulan)
  - **Frontend**: Vercel / Netlify (free, custom domain)
  - Setup environment variables di tiap platform
  - Update CORS di FastAPI agar align dengan domain frontend
- **Effort**: 2-4 jam (tergantung kendala deployment)
- **Owner**: Rifqi (Full-Stack), Anda (env vars)

### P2-2. Deployment Streamlit Cloud
- **Source**: Worksheet DS Side Quest — "deployment dashboard ke Streamlit Cloud"
- **Status saat ini**: Dashboard cuma jalan lokal di port 8501
- **Yang dilakukan**:
  - Push dashboard ke GitHub (sudah ada)
  - Sign up Streamlit Cloud (gratis, butuh akun GitHub)
  - Connect repo, point ke `dashboard/app.py`
  - Tambahkan `requirements.txt` minimal di `dashboard/`
  - Get public URL
- **Effort**: ~30 menit
- **Owner**: Anda

### P2-3. SHAP Analysis Lengkap + Interpretasi
- **Source**: Mentor Notes poin 3 — "SHAP TreeExplainer untuk argumen pemilihan fitur di presentasi"
- **Status saat ini**: SHAP plot generated tapi belum optimal (sample kecil, perlu re-run)
- **Yang dilakukan**:
  - Re-run `generate_shap_analysis.py` setelah model final dipilih
  - Verify output di `reports/`: `shap_summary_bar.png`, `shap_summary_beeswarm.png`, `shap_interpretation.md`
  - Embed di slide presentasi
- **Effort**: ~30 menit (script ready)
- **Owner**: Anda

### P2-4. Custom Training Loop dengan `tf.GradientTape`
- **Source**: Worksheet AI Side Quest
- **Status saat ini**: Belum ada
- **Yang dilakukan**: Buat notebook 08 atau script terpisah yang implement custom training loop:
  ```python
  with tf.GradientTape() as tape:
      pred = model(X, training=True)
      loss = focal_loss(y, pred)
  grads = tape.gradient(loss, model.trainable_variables)
  optimizer.apply_gradients(zip(grads, model.trainable_variables))
  ```
- **Effort**: 1-2 jam
- **Owner**: AI Engineer (Fathan/Shafira) atau Anda

### P2-6. Eksperimen 6 Variasi Model DL + Tuning
- **Source**: Mentoring 1 #4 + #5 + #7 — "pemilihan model final berbasis data, bukan asumsi"
- **Status saat ini**: ❌ Kita baru benchmark 4 model (LR, DT, RF, DL baseline). Belum ada variasi arsitektur DL untuk justifikasi pemilihan.
- **Mengapa P2**: Mentor ingin model selection berbasis bukti. Comparison table akan jadi argumen kuat di slide #8 (Benchmark) dan laporan PDF #9 (DL section). Bukan blocker submission tapi significantly memperkuat narrative.
- **Yang dilakukan**: Train 6 varian dan compare metrik (Accuracy, Precision, Recall, F1, ROC-AUC) di X_test sama:
  | Varian | Arsitektur | Tuning |
  |---|---|---|
  | 1. **Baseline (current)** | Dense[256-128-64-1] + BN + Dropout 0.3 | DL+SMOTE @ thr 0.23 |
  | 2. **Shallow NN** | Dense[64-1] + Dropout 0.3 | Sama |
  | 3. **Deep NN** | Dense[512-256-128-64-32-1] + BN + Dropout 0.3 | Sama |
  | 4. **Wide NN** | Dense[512-512-1] + BN + Dropout 0.3 | Sama |
  | 5. **No BatchNorm** | Dense[256-128-64-1] + Dropout 0.3 | Sama |
  | 6. **No Dropout sebelum output** | Dense[256-128-64-1] + BN + Dropout (kecuali sebelum output) | Sama |
  - Tambah eksperimen tuning: **CosineDecay LR scheduler** (sebagai alternative ReduceLROnPlateau yang gagal kita)
  - Output: `reports/dl_experiments.json` + `reports/dl_experiments_comparison.png`
  - Embed hasil di laporan PDF (P1-1) section "DL Experimentation" dan slide #8 (Benchmark)
- **Effort**: 3-5 jam (5 model × ~30 menit train + compare + plot)
- **Owner**: AI Engineer (Fathan/Shafira) atau Anda
- **Note**: Bisa di-skip kalau waktu sangat terbatas — current DL+SMOTE @ 0.23 sudah penuhi target. Tapi kalau dikerjakan, jadi nilai tambah signifikan di laporan.

### P2-5. TensorBoard Log Commit ke Repository
- **Source**: Worksheet AI Side Quest — "menyertakan log yang dihasilkan dalam repository akhir"
- **Status saat ini**: Log ada di `ml-api/tensorboard_logs/` tapi sudah di `.gitignore`
- **Yang dilakukan**:
  - Un-ignore `tensorboard_logs/` di `.gitignore`
  - Atau pindah subset log terbaik ke folder yang tracked
  - Commit & push
- **Effort**: 5-10 menit
- **Owner**: Anda

---

## 🟢 P3 — LOWER URGENCY (Nice to have)

> Item bonus untuk ekstra nilai, kerjakan kalau ada waktu.

### P3-0. Halaman News/Edukasi di Web App
- **Source**: Mentoring 1 #2 — "News/Edukasi (nice to have)" sebagai halaman ke-4 di struktur aplikasi
- **Status saat ini**: ❌ Belum ada. Struktur app saat ini: Home → Prediksi → (Visualisasi, P1-6)
- **Yang dilakukan**:
  1. Tambah route `/news` di react-router (App.jsx)
  2. Buat `NewsPage.jsx` dengan konten statis atau dari data JSON:
     - Artikel edukasi: apa itu faktor risiko jantung, pentingnya deteksi dini, gaya hidup sehat
     - Link sumber terpercaya (Kemenkes, WHO, AHA)
     - Card layout sederhana (tidak perlu API)
  3. Update Navbar: tambah link "Edukasi" setelah "Insights"
- **Effort**: ~1 jam (konten statis, no backend needed)
- **Owner**: Full-Stack (Rifqi/Shafira) atau Anda

### P3-1. Verifikasi Responsive Layout
- **Source**: Role path.pdf Side Quest FE — "Membangun layout aplikasi web yang responsif"
- **Status saat ini**: ⚠️ Tailwind `sm:`/`lg:` breakpoints sudah dipakai di kode, tapi belum pernah diverifikasi eksplisit di mobile viewport
- **Yang dilakukan**: Buka DevTools → toggle mobile view (375px, 768px) → test Landing, Form (5 step), Result → pastikan tidak ada overflow/layout break
- **Effort**: ~15 menit
- **Owner**: Anda (bisa dilakukan bersamaan dengan P0-1 browser test)

### P3-2. Mockup UI/UX di Figma
- **Source**: Worksheet Front-End Side Quest
- **Status saat ini**: Belum ada (langsung implement)
- **Yang dilakukan**: Bikin mockup Figma untuk Landing/Form/Result page (3 screens)
- **Effort**: 1-2 jam
- **Owner**: Full-Stack (Rifqi/Shafira)

### P3-3. REST API + Database (history prediksi)
- **Source**: Worksheet Front-End Side Quest
- **Status saat ini**: Belum ada DB
- **Yang dilakukan**: Add endpoint `POST /api/history`, `GET /api/history/:userId` + integrasi MongoDB/PostgreSQL
- **Effort**: 2-3 jam
- **Owner**: Rifqi

### P3-4. MAE ≤ 0.02 Performance Target
- **Source**: Worksheet AI Side Quest
- **Status saat ini**: Belum dihitung. **Sulit dicapai** karena binary classification (typical MAE 0.1-0.3)
- **Yang dilakukan**: Compute MAE dan dokumentasikan di laporan + slide kenapa tidak tercapai (matematis: MAE binary class minimum sekitar class imbalance ratio)
- **Effort**: ~15 menit (compute + justifikasi)
- **Owner**: Anda

### P3-5. Update Dashboard Streamlit dengan Section "Live Prediction"
- **Source**: Improvement initiative (bukan dari worksheet/mentor)
- **Status saat ini**: Dashboard cuma EDA, belum ada inference section
- **Yang dilakukan**: Add section yang call ke ml-api untuk demo prediksi langsung di dashboard
- **Effort**: ~45 menit
- **Owner**: Anda

---

## 📊 Summary

| Priority | Total Items | Estimated Total Effort |
|---|---|---|
| 🚨 P0 | 1 | 30 menit |
| 🔴 P1 | 6 | 10-14 jam |
| 🟡 P2 | 6 | 7-13 jam |
| 🟢 P3 | 6 | 5-9 jam |
| **Total** | **19** | **23-37 jam** |

### Yang sudah selesai (untuk reference):
- ✅ Notebooks 01-07 (DS + AI Engineer)
- ✅ Feature engineering (6 fitur baru)
- ✅ DL+SMOTE training @ threshold 0.23 (Acc 85.76%, Recall 71.15%, ROC-AUC 0.881)
- ✅ Custom components (Focal Loss + EarlyStoppingByRecall)
- ✅ FastAPI dengan SHAP + Gemini AI + Lifestyle Score
- ✅ Inference time optimization (7s → 350ms)
- ✅ Frontend (Vite + React + Tailwind + react-router + framer-motion + 3D)
- ✅ Form tooltips + BMI auto-preview
- ✅ ResultPage dual-score (Lifestyle Score primary)
- ✅ Express backend proxy
- ✅ Streamlit dashboard running (lokal)
- ✅ Smoke test E2E API
- ✅ A/B Testing notebook
- ✅ Data Dictionary
- ✅ PDF analysis report (validasi threshold)

---

## 🎯 Rekomendasi Eksekusi 1-2 Minggu Terakhir

**Week 1 (sisa minggu ini) — focus on application & content:**
- Hari 1: P0-1 (browser test) + **P1-5** (Gemini aktivasi + loading + konsistensi) + P3-3 (MAE doc) + P2-5 (TensorBoard commit)
- Hari 2: **P1-6** (Halaman Visualisasi Data web)
- Hari 3: P2-3 (SHAP final analysis) + P2-2 (Streamlit Cloud deploy)
- Hari 4: P1-4 (Business narrative research)
- Hari 5: P2-1 (Deployment ml-api + backend + frontend)

**Week 2 (sebelum hari demo) — focus on presentation & polish:**
- Hari 1: P1-1 (Laporan PDF komprehensif) — half
- Hari 2: P1-1 (lanjutan) + P1-2 (Slide outline & content)
- Hari 3: P1-2 (Slide visual di Canva) + P1-3 (Q&A document)
- Hari 4: **P2-6** (Eksperimen 6 variasi DL — kalau ada waktu)
- Hari 5: Latihan presentasi + polish UI/dokumen
- Hari 6: P2-4 (tf.GradientTape, kalau masih ada waktu) + P3-1 (Mockup, kalau ada waktu)
- Hari 7 (D-Day): Demo
