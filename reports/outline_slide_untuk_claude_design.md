# Outline Presentasi Pulsevera — untuk Claude Design
> Updated: sesuai persyaratan resmi Coding Camp 2026

> **Instruksi Claude Design:** Buatkan presentasi pitch deck profesional 12 slide berdasarkan outline berikut. Gunakan palet warna merah (#EF4444) dan indigo (#4F46E5) dengan aksen hijau (#10B981). Font modern sans-serif (Plus Jakarta Sans / Inter). Layout bersih, data-driven, startup tech feel. Aktifkan speaker notes untuk setiap slide.

---

## IDENTITAS

- **Judul**: Pulsevera — Deteksi Dini Risiko Jantung Berbasis AI
- **Tagline**: "Jantungmu, Cerita Masa Depanmu."
- **Acara**: Demo Day Coding Camp 2026 powered by DBS Foundation
- **Tim**: CC26-PRU439
- **Warna**: Merah `#EF4444` · Indigo `#4F46E5` · Hijau `#10B981` · Putih `#FFFFFF`
- **Font**: Plus Jakarta Sans atau Inter
- **Durasi**: 12–15 menit + 5 menit Q&A

---

## SLIDE 1 — COVER

**Layout:** Full-bleed gradient merah ke indigo
**Elemen:**
- Nama: PULSEVERA (font display, bold, putih, besar)
- Tagline: *"Jantungmu, Cerita Masa Depanmu."*
- Subtitle: Deteksi Dini Risiko Penyakit Jantung Berbasis AI
- Badge: CC26-PRU439 · DBS Foundation Coding Camp 2026
- Visual: ikon jantung 3D minimalis di sisi kanan
- Nama anggota tim di pojok kiri bawah

**Speaker notes:** Mulai dengan senyum dan konfiden. Slide ini adalah kesan pertama — biarkan desain berbicara selama 5 detik sebelum mulai berbicara.

---

## SLIDE 2 — LATAR BELAKANG

**Judul:** Krisis Diam-Diam: Penyakit Jantung di Indonesia
**Layout:** 4 big number cards (grid 2×2) + 1 trend box di bawah

**4 Statistik kunci:**
- 🫀 **635.000** kematian/tahun akibat CVD · WHO 2023
- ⚡ **40%** serangan fatal sebelum sempat ke RS · AHA 2024
- 💰 **Rp 30–150 juta** biaya perawatan per episode · BPJS 2022
- 👥 **1 dari 3** penderita tidak mengetahui risikonya · Riskesdas 2019

**Trend box (highlight):**
- Tren global: CVD meningkat 17.1% dalam 10 tahun terakhir (GBD 2022)
- Indonesia: CVD adalah beban terbesar BPJS Kesehatan sejak 2017
- Penelitian: ML untuk prediksi CVD terbukti efektif (AHA Scientific Statement 2021)
- Gap: Tools yang ada memerlukan data klinis — tidak accessible masyarakat awam

**Speaker notes:** Angka 635.000 setara kota Samarinda hilang setiap tahun. Pause setelah angka ini. Emphasize "tidak menyadari" — ini gap utama yang Pulsevera isi. Riset menunjukkan ML bisa menjadi solusi accessible.

---

## SLIDE 3 — RUMUSAN MASALAH

**Judul:** Mengapa Risiko Jantung Tidak Terdeteksi?
**Layout:** 3 kolom icon + teks

**Kolom 1 — Akses Terbatas** 🏥
- Screening EKG/echo: Rp 300K–2,5 juta
- Hanya tersedia di RS tipe B/C ke atas
- Rasio dokter jantung: 1:1,2 juta (luar Jawa)

**Kolom 2 — Kesadaran Rendah** 🧑‍💼
- Generasi 25–34: "masih muda, belum perlu"
- Faktor risiko terbentuk sejak usia 20-an
- Tidak ada early warning personal yang digital

**Kolom 3 — No Digital Solution** ⚡
- 40% serangan pertama langsung fatal
- Tools yang ada butuh pengetahuan klinis
- Tidak ada yang ramah pengguna awam Indonesia

**Rumusan masalah (callout box):**
> "Bagaimana membuat skrining risiko jantung yang accessible, personal, dan berbasis data — tanpa memerlukan alat medis atau pengetahuan klinis?"

**Speaker notes:** Ketiga gap ini saling berkaitan. Gap 3 adalah akibat dari gap 1 dan 2. Emphasize bahwa ini bukan masalah yang tidak bisa diselesaikan — teknologi sudah ada.

---

## SLIDE 4 — PERBANDINGAN PRODUK SERUPA

**Judul:** Solusi yang Ada Belum Cukup
**Layout:** Tabel perbandingan 5 kolom

| Aspek | Halodoc / Alodokter | WHO CVD Calculator | Framingham Score | **Pulsevera** |
|---|---|---|---|---|
| Akses | Perlu akun/login | Web statis, Inggris | Kalkulator manual | Browser, tanpa login |
| Bahasa | Indonesia | Inggris | Inggris | **Indonesia** |
| Input | Konsultasi dokter | Data klinis (kolesterol, tekanan darah) | Data klinis | **10 pertanyaan harian** |
| Output | Rujukan dokter | Skor angka saja | % risiko 10 tahun | **Dual metric + rekomendasi AI** |
| Explainability | Tidak ada | Tidak ada | Formula tersembunyi | **SHAP per prediksi** |
| Personalisasi AI | Tidak ada | Tidak ada | Tidak ada | **Gemini 2.5 Flash** |
| Biaya | Berbayar (konsultasi) | Gratis | Gratis | **Gratis** |

**Callout (keunggulan Pulsevera):**
> Pulsevera adalah satu-satunya yang menggabungkan: data populasi besar (445K) + ML tervalidasi + SHAP explainability + Gemini AI + bahasa Indonesia + tanpa data klinis

**Speaker notes:** Jangan menyerang produk lain secara negatif. Frame sebagai "mereka bagus di domain mereka, tapi ada gap yang belum terisi." Pulsevera mengisi gap spesifik: accessible + explainable + Indonesian context.

---

## SLIDE 5 — SOLUSI: PULSEVERA

**Judul:** Pulsevera: Deteksi Dini dalam 2 Menit
**Layout:** 4 step flow di kiri, mockup/screenshot di kanan

**4 Langkah:**
1. 📝 Isi 10 pertanyaan gaya hidup (< 2 menit)
2. 🤖 AI analisis: DL model + SHAP attribution
3. 📊 Skor Gaya Hidup (0–5) + Estimasi Risiko
4. 💡 Rekomendasi personal (Gemini AI)

**Value proposition:**
| | Sebelum Pulsevera | Dengan Pulsevera |
|---|---|---|
| Akses | Ke RS/klinik | Langsung di browser |
| Biaya | Rp 300K+ | Gratis |
| Waktu | 1–3 jam | < 2 menit |
| Output | Angka klinis | Bahasa awam + actionable |

**Badge disclaimer:** ⚠️ Alat edukasi — bukan pengganti dokter

**Speaker notes:** Demo singkat di sini jika memungkinkan. Emphasize "10 pertanyaan dari kehidupan sehari-hari" — bukan pertanyaan klinis. User tidak perlu tahu tekanan darahnya.

---

## SLIDE 6 — TARGET USER & DAMPAK

**Judul:** Untuk Siapa, dan Dampaknya?
**Layout:** 2 persona kiri + impact funnel kanan

**Persona Kiri:**
👔 **"Rafi"** — Urban Professional 25–34
- Kerja 8+ jam/hari, jarang olahraga, kadang merokok
- Digital native, tidak pernah cek jantung

👩‍👧 **"Sinta"** — Keluarga Pasien CVD 35–50
- Ada anggota keluarga pernah serangan jantung
- Aktif mencari informasi preventif

**Impact Funnel Kanan:**
```
60 juta penduduk Indonesia usia 25–45
         ↓ 0.1% adoption
     60.000 user
         ↓ 5% terdeteksi risiko tinggi
     3.000 potensi intervensi dini
         ↓
  Hemat 10–50× biaya darurat CVD
```

**Speaker notes:** Frame sebagai "dampak potensial" bukan klaim. 1 orang yang terdeteksi dini dan berubah gaya hidup = investasi kesehatan terbaik.

---

## SLIDE 7 — DATASET & PEMILIHAN FITUR

**Judul:** Data yang Solid, Fitur Tervalidasi SHAP
**Layout:** Info dataset kiri, SHAP chart kanan

**Kiri — Dataset CDC BRFSS 2022:**
- 🏛️ Survei resmi Centers for Disease Control (CDC)
- 📊 445.132 responden nyata
- 40+ variabel perilaku kesehatan
- Target: HadHeartAttack (5.6% positif — imbalanced)
- Pembagian: 80% train / 20% test (stratified)

**Kanan — Top SHAP Features:**
1. Kondisi Kesehatan Umum — 0.111
2. Kategori Usia — 0.076
3. Riwayat Diabetes — 0.058
4. Konsumsi Alkohol — 0.048
5. Aktivitas Fisik — 0.039
6. Jam Tidur — 0.016

**Visual:** Embed `shap_summary_bar.png`

**Footer:** *"10 field form mencakup mayoritas top SHAP features — divalidasi secara kuantitatif, bukan subjektif"*

**Speaker notes:** SHAP membuktikan bahwa pilihan fitur form kami bukan asal-asalan. Fitur klinis (angina, stroke) tidak ditanyakan karena UX — user awam tidak tahu apakah pernah angina.

---

## SLIDE 8 — BENCHMARK MODEL

**Judul:** Mengapa Deep Learning? Data Berbicara.
**Layout:** Tabel benchmark + callout menonjol

**Tabel (highlight baris DL):**
| Model | Accuracy | **Recall** | F1 | ROC-AUC |
|---|---|---|---|---|
| Logistic Regression | 84.2% | 64.6% | 31.6% | 83.1% |
| Decision Tree | 82.8% | 62.8% | 29.2% | 81.3% |
| Random Forest | 90.9% | 44.5% | 35.6% | 84.6% |
| **DL + SMOTE ✓** | **85.8%** | **71.2%** | **36.1%** | **88.1%** |

**Callout box (warna merah, menonjol):**
> ⚠️ Random Forest accuracy 90.9% — tapi Recall hanya 44.5%
> = 56 dari 100 orang berisiko **TIDAK TERDETEKSI**
> Untuk medical screening: **Recall > Accuracy**

**Mini diagram bawah:**
- False Negative = gagal deteksi orang berisiko → berbahaya
- False Positive = salah flag orang sehat → bisa diverifikasi dokter

**Speaker notes:** Ini slide kunci yang akan ditanya juri. Jelaskan dengan tenang bahwa accuracy tinggi bisa "menipu" pada imbalanced dataset. Pause setelah kata "TIDAK TERDETEKSI."

---

## SLIDE 9 — MODEL FINAL & THRESHOLD

**Judul:** DL + SMOTE @ Threshold 0.23 — Sweet Spot
**Layout:** Arsitektur vertikal kiri, metrics + chart kanan

**Kiri — Arsitektur:**
```
Input (46 fitur)
↓
Dense 256 + BatchNorm + Dropout 0.3
↓
Dense 128 + BatchNorm + Dropout 0.3
↓
Dense 64 + Dropout 0.15
↓
Dense 1 (Sigmoid) → Threshold @ 0.23
```

**Custom Components:**
- 🔥 Focal Loss (γ=2.0, α=0.25) — hukum easy negatives
- 🛑 EarlyStoppingByRecall — stop saat recall stagnan

**Training Strategy:**
- SMOTE (sampling_strategy=0.3)
- class_weight balanced (class 1 = 2.17×)

**Kanan — Final Metrics:**
| Metrik | Nilai | Target | Status |
|---|---|---|---|
| Accuracy | 85.76% | ≥ 85% | ✅ |
| Recall | 71.15% | ≥ 70% | ✅ |
| ROC-AUC | 88.12% | ≥ 80% | ✅ |

**Visual:** Embed `fig_threshold_curves.png`

**Speaker notes:** Threshold 0.23 bukan angka sembarangan — hasil eksperimen sistematis. Tunjukkan grafik threshold curves. Emphasize dua target program terpenuhi sekaligus.

---

## SLIDE 10 — HASIL PENGEMBANGAN & DEMO

**Judul:** Pulsevera — Live & Bisa Dicoba Sekarang
**Layout:** 4 screenshot alur + URL + QR code

**Screenshot 1:** Landing page — tagline + 3D heart + CTA
**Screenshot 2:** Form (step Antropometri, BMI auto-preview)
**Screenshot 3:** Hasil — Lifestyle Score gauge + 5 habits checklist
**Screenshot 4:** Hasil — Rekomendasi Gemini AI

**Flow narasi:**
> User 28 tahun, perokok aktif, tidak olahraga
> → Isi form 2 menit
> → Lifestyle Score: 1/5 "Berisiko Tinggi"
> → Rekomendasi spesifik dari Gemini AI

**Mengapa implementasi ini:**
- React + Three.js: UX modern, 3D heart sebagai brand identity
- FastAPI: performa tinggi, ~350ms inference
- SHAP: transparansi prediksi, bukan black box
- Gemini AI: rekomendasi yang terasa personal

**QR + URL besar:**
🌐 **pulsevera.vercel.app**

**Speaker notes:** Kalau bisa, buka browser langsung dan demo live. Siapkan data user "Rafi" (28 tahun, perokok) sebagai contoh. Jika koneksi buruk, gunakan screenshot saja.

---

## SLIDE 11 — DOKUMENTASI

**Judul:** Open Source & Reproducible
**Layout:** 2 kolom — GitHub info kiri, cara replikasi kanan

**Kiri — Repository:**
- 🐙 GitHub: `github.com/muhamadtegar1/pulsevera-CC26-PRU439`
- Branch: `main` (production-ready)
- README.md: setup guide lengkap
- Struktur: `frontend/` · `backend/` · `ml-api/` · `notebooks/` · `reports/`

**Kanan — Cara Replikasi (dari README):**
```bash
# Clone repo
git clone https://github.com/muhamadtegar1/
              pulsevera-CC26-PRU439

# ML API
cd ml-api && pip install -r requirements.txt
uvicorn main:app --port 8000

# Backend
cd backend && npm install && npm run dev

# Frontend
cd frontend && npm install && npm run dev
```

**Deployment live:**
| Service | URL |
|---|---|
| Frontend | pulsevera.vercel.app |
| ML API | tgrrr-pulsevera-ml-api.hf.space |
| Backend | tgrrr-pulsevera-backend.hf.space |

**Speaker notes:** Emphasize bahwa proyek ini open source dan reproducible. Juri bisa clone dan jalankan sendiri. README mencakup semua langkah dari install hingga deploy.

---

## SLIDE 12 — RENCANA IMPLEMENTASI (Opsional)

**Judul:** Pulsevera: Dari Capstone ke Produk Nyata
**Layout:** Timeline 3 fase + resource tabel

**Fase 1 — Short Term (3–6 bulan):**
- History tracking (opsional, dengan consent user)
- Fine-tuning model dengan data Indonesia
- Halaman edukasi CVD
- Mobile-responsive optimization

**Fase 2 — Mid Term (6–12 bulan):**
- Mobile app (React Native)
- Kemitraan dengan Puskesmas/FKTP
- Validasi klinis oleh tenaga medis
- API untuk integrasi sistem kesehatan

**Fase 3 — Long Term (1–2 tahun):**
- Kemitraan BPJS Kesehatan (program preventif)
- Dataset Indonesia untuk re-training
- Integrasi ICD-10 / rekam medis digital

**Resource estimate:**
| Resource | Kebutuhan | Sumber |
|---|---|---|
| Tim | 2 dev + 1 data scientist | Internal |
| Infrastruktur | Cloud (HF Spaces + Vercel) | Gratis/low cost |
| Data Indonesia | Kolaborasi Kemenkes/RS | Partnership |
| Validasi klinis | 1 dokter spesialis jantung | Konsultasi |

**Speaker notes:** Frame ini sebagai visi, bukan janji. Emphasize bahwa MVP sudah berjalan — ini bukan sekadar ide, sudah ada produk nyata yang bisa diakses hari ini.

---

## SLIDE BONUS A — PROJECT OVERVIEW (Checklist Penjurian)

**Judul:** Checklist Program — Semua Terpenuhi
**Layout:** 2 kolom checklist

**Main Quest ✅**
- Deep Learning (TF Functional API)
- Custom Component (Focal Loss + Callback)
- RESTful API (FastAPI + Express)
- Networking (Axios)
- Module Bundler (Vite)
- Data Wrangling, EDA, Dashboard

**Side Quest ✅**
- FastAPI Standalone ML API
- Generative AI (Gemini 2.5 Flash)
- A/B Testing (4 hipotesis)
- Feature Engineering (6 fitur baru)
- SHAP Analysis
- Custom Training Loop (tf.GradientTape)
- 6 DL Architecture Experiments
- Full Deployment (HF Spaces + Vercel)
- Laporan Teknis Komprehensif

---

## SLIDE BONUS B — ARSITEKTUR SISTEM

**Judul:** System Architecture
**Layout:** Diagram alur horizontal

```
[User Browser]
React 18 + Vite + Tailwind + Three.js
      ↓ HTTPS / Axios
[Express.js Backend — HF Spaces]
Proxy · CORS · Rate limiting
      ↓ HTTP
[FastAPI ML API — HF Spaces]
Preprocessing → DL Keras → SHAP → Gemini AI
      ↓ JSON Response
[Result Page]
Lifestyle Score · Risk Score · Recommendations
```

**Deployment:**
- Frontend → Vercel (auto-deploy dari GitHub)
- Backend → HF Spaces Docker (Node 20)
- ML API → HF Spaces Docker (Python 3.11 + TF 2.17)

---

## CATATAN UNTUK DESAINER

**Palet warna:**
- Primary: `#4F46E5` (indigo)
- Heart/Danger: `#EF4444` (red)
- Success: `#10B981` (green)
- Warning: `#F59E0B` (amber)
- Background: `#FAFAFA` atau gradient ke `#EFF6FF`
- Text: `#0F172A`

**Style:** Startup pitch deck modern, bukan academic poster. Whitespace luas, data = visual bukan teks panjang, setiap slide 1 pesan utama.

**Assets untuk di-embed:**
- `reports/shap_summary_bar.png` → Slide 7
- `reports/fig_threshold_curves.png` → Slide 9
- `reports/fig_confusion_matrix.png` → Slide 9
- `reports/dl_experiments_comparison.png` → Slide 8
- Screenshot app → Slide 10 (ambil dari pulsevera.vercel.app)
