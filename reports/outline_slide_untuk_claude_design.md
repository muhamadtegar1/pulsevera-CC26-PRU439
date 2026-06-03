# Outline Presentasi Pulsevera — untuk Claude Design

> **Instruksi:** Gunakan outline ini sebagai brief untuk Claude Design atau Canva AI. Katakan: *"Buatkan presentasi pitch deck professional 10 slide berdasarkan outline berikut. Gunakan palet warna merah (#EF4444) dan indigo (#4F46E5), dengan aksen hijau (#10B981). Font modern sans-serif. Layout bersih, data-driven, startup tech feel."*

---

## IDENTITAS

- **Judul**: Pulsevera — Deteksi Dini Risiko Jantung Berbasis AI
- **Tagline**: "Jantungmu, Cerita Masa Depanmu."
- **Acara**: Demo Day Coding Camp 2026, DBS Foundation
- **Tim**: CC26-PRU439
- **Warna brand**: Merah `#EF4444`, Indigo `#4F46E5`, Hijau `#10B981`, Putih `#FFFFFF`
- **Font**: Plus Jakarta Sans atau Inter
- **Durasi presentasi**: 12 menit + 5 menit Q&A

---

## SLIDE 1 — COVER

**Layout:** Full-bleed dengan gradient merah-indigo
**Elemen:**
- Logo/nama: PULSEVERA (font display, bold, putih)
- Tagline: "Jantungmu, Cerita Masa Depanmu."
- Subtitle: Deteksi Dini Risiko Penyakit Jantung Berbasis AI
- Badge: CC26-PRU439 · DBS Foundation Coding Camp 2026
- Visual: Ilustrasi 3D heart atau ikon jantung minimalis
- Nama tim di pojok bawah

---

## SLIDE 2 — THE PROBLEM

**Judul:** Penyakit Jantung: Krisis Kesehatan #1 Indonesia
**Layout:** 4 big number cards dalam grid 2×2

**4 Statistik utama:**
- 🫀 **635.000** kematian/tahun · Sumber: WHO 2023
- ⚡ **40%** serangan fatal sebelum sampai RS · Sumber: AHA 2024
- 💰 **Rp 30–150 juta** biaya per episode perawatan · Sumber: BPJS 2022
- 👥 **1 dari 3** penderita tidak mengetahui risikonya · Sumber: Riskesdas 2019

**Pull quote di bawah:**
> "Penyakit jantung sangat bisa dicegah — tapi mayoritas orang tidak tahu risikonya sampai terlambat."

---

## SLIDE 3 — PROJECT OVERVIEW (Khusus Penjurian)

**Judul:** Pulsevera — Solusi Berbasis Data
**Layout:** 2 kolom (Tech Stack kiri, Checklist kanan)

**Kiri — Tech Stack:**
```
Frontend  : React + Vite + Tailwind + Three.js
Backend   : Express.js (proxy)
ML API    : FastAPI + TensorFlow
Dataset   : CDC BRFSS 2022 · 445K sampel
AI        : Google Gemini 2.5 Flash
Deploy    : HF Spaces + Vercel
```

**Kanan — Checklist:**
- ✅ Deep Learning (TF Functional API + Custom Loss)
- ✅ RESTful API (FastAPI + Express)
- ✅ Generative AI (Gemini)
- ✅ A/B Testing & Feature Engineering
- ✅ SHAP Explainability
- ✅ Full Deployment (Live di cloud)

---

## SLIDE 4 — PROBLEM DEFINITION

**Judul:** 3 Gap yang Membiarkan Risiko Tidak Terdeteksi
**Layout:** 3 kolom icon + teks

**Kolom 1 — Akses Terbatas**
Ikon: 🏥
- EKG/echo: Rp 300K–2,5 juta
- Hanya RS tipe B/C ke atas
- Rasio dokter jantung 1:1,2 juta (luar Jawa)

**Kolom 2 — Kesadaran Rendah**
Ikon: 🧑‍💼
- 25–34 tahun: "masih muda, belum perlu"
- Faktor risiko terbentuk sejak usia 20-an
- Tidak ada tools personal berbasis data

**Kolom 3 — No Early Warning**
Ikon: ⏰
- 40% serangan pertama langsung fatal
- Tidak ada titik sentuh preventif digital
- Gap 1 + 2 menyebabkan Gap 3

---

## SLIDE 5 — OUR SOLUTION

**Judul:** Pulsevera: Cek Risiko Jantung dalam 2 Menit
**Layout:** Mockup smartphone di kanan, 4 steps di kiri

**4 Langkah:**
1. 📝 Isi 10 pertanyaan gaya hidup harian
2. 🤖 AI analisis dengan DL + SHAP
3. 📊 Dapat Skor Gaya Hidup (0–5) + Risk Score
4. 💡 Rekomendasi personal dari Gemini AI

**Tabel perbandingan (small):**
| | Klinik Tradisional | Pulsevera |
|---|---|---|
| Akses | Perlu antri, biaya | Browser, gratis |
| Waktu | 1–3 jam | < 2 menit |
| Output | Angka klinis | Skor gaya hidup |

**Badge disclaimer:** ⚠️ Bukan pengganti dokter

---

## SLIDE 6 — IMPACT & TARGET USER

**Judul:** Untuk Siapa, dan Dampaknya?
**Layout:** 2 persona di kiri, impact calculator di kanan

**Persona Kiri:**
👔 **"Rafi"** — Urban Professional 25–34
- Kerja 8+ jam/hari, jarang olahraga
- Digital native, tidak pernah screening jantung

👩‍👧 **"Sinta"** — Keluarga Pasien CVD
- Ada anggota keluarga pernah serangan jantung
- Aktif mencari tools preventif

**Impact Calculator Kanan (visual funnel):**
```
60 juta penduduk usia 25–45
     ↓ 0.1% adoption
60.000 user
     ↓ 5% terdeteksi risiko tinggi
3.000 potensi intervensi dini
     ↓
Hemat 10–50x biaya darurat CVD
```

---

## SLIDE 7 — DATA & FEATURE SELECTION

**Judul:** Data Solid, Fitur Tervalidasi SHAP
**Layout:** Split — dataset info kiri, SHAP chart kanan

**Kiri — Dataset:**
- CDC BRFSS 2022 (CDC, USA)
- 445.132 responden nyata
- 40+ variabel perilaku kesehatan
- Target: HadHeartAttack (5.6% positif)

**Kanan — SHAP Top Features (bar chart mini):**
1. Kondisi Kesehatan Umum — 0.111
2. Kategori Usia — 0.076
3. Riwayat Diabetes — 0.058
4. Konsumsi Alkohol — 0.048
5. Aktivitas Fisik — 0.039
6. Jam Tidur — 0.016

**Footer note:** *"10 field form dipilih karena merupakan keseharian — divalidasi secara kuantitatif via SHAP"*

---

## SLIDE 8 — MODEL BENCHMARK

**Judul:** Mengapa Deep Learning? Data Berbicara.
**Layout:** Tabel benchmark + callout box

**Tabel (highlight baris DL):**
| Model | Accuracy | **Recall** | ROC-AUC |
|---|---|---|---|
| Logistic Regression | 84.2% | 64.6% | 83.1% |
| Decision Tree | 82.8% | 62.8% | 81.3% |
| Random Forest | 90.9% | 44.5% | 84.6% |
| **DL + SMOTE ✓** | **85.8%** | **71.2%** | **88.1%** |

**Callout box (menonjol):**
> Random Forest accuracy 90.9% — tapi Recall hanya 44.5%
> = 56 dari 100 orang berisiko TIDAK TERDETEKSI ❌
> Untuk medical screening, Recall > Accuracy

**Mini diagram:** False Negative = berbahaya, False Positive = bisa diverifikasi

---

## SLIDE 9 — MODEL FINAL & THRESHOLD

**Judul:** DL + SMOTE @ Threshold 0.23 — Sweet Spot
**Layout:** Arsitektur kiri, threshold chart kanan

**Kiri — Arsitektur (diagram vertikal):**
```
Input (46 fitur)
↓
Dense 256 + BN + Dropout 0.3
↓
Dense 128 + BN + Dropout 0.3
↓
Dense 64 + Dropout 0.15
↓
Dense 1 (Sigmoid)
↓
Threshold @ 0.23
```

**Custom components:**
- 🔥 Focal Loss (γ=2.0, α=0.25)
- 🛑 EarlyStoppingByRecall

**Kanan — Final Metrics:**
- ✅ Accuracy: **85.76%** (target ≥ 85%)
- ✅ Recall: **71.15%** (target ≥ 70%)
- ✅ ROC-AUC: **88.12%** (excellent)

---

## SLIDE 10 — LIVE DEMO

**Judul:** Pulsevera — Coba Sekarang
**Layout:** 4 screenshot alur aplikasi secara berurutan

**Screenshot 1:** Landing page — tagline + CTA button
**Screenshot 2:** Form step (BMI auto-preview)
**Screenshot 3:** Hasil — Lifestyle Score gauge 3/5
**Screenshot 4:** Hasil — Rekomendasi Gemini AI

**Flow narasi slide:**
> User 28 tahun, perokok aktif, tidak olahraga
> → Isi form 2 menit
> → Lifestyle Score: 1/5 "Berisiko Tinggi"
> → Rekomendasi: "Mulai dengan berhenti merokok dan 30 menit jalan kaki per hari"

**QR Code + URL:**
🌐 **pulsevera.vercel.app**

**Closing statement:**
> *"Pulsevera bukan tentang menakut-nakuti. Ini tentang memberi tahu — dengan data, dengan transparansi, dan dengan kepedulian."*

---

## SLIDE BONUS — Arsitektur Sistem

**Judul:** System Architecture
**Layout:** Diagram alur horizontal

```
[User Browser]
React + Vite + Tailwind
      ↓ HTTPS
[Express.js Backend]
Proxy · CORS · Middleware
      ↓ HTTP
[FastAPI ML API]
Preprocessing → DL Inference → SHAP → Gemini
      ↓ JSON
[Result Page]
Lifestyle Score + Risk Score + Recommendations
```

**Deployment row di bawah:**
- Frontend: Vercel · pulsevera.vercel.app
- Backend: HF Spaces
- ML API: HF Spaces
- Code: GitHub

---

## CATATAN UNTUK DESAINER

**Palet warna:**
- Primary: `#4F46E5` (indigo — pulse brand)
- Danger/Heart: `#EF4444` (red)
- Success: `#10B981` (green/mint)
- Warning: `#F59E0B` (amber)
- Background: `#FAFAFA` atau gradient putih ke `#EFF6FF`
- Text: `#0F172A` (dark)

**Style:** Modern tech startup pitch deck, bukan academic poster. Banyak whitespace, data ditampilkan dengan visual bukan teks panjang.

**Assets tersedia:**
- Screenshot app: ambil dari https://pulsevera.vercel.app
- SHAP chart: `reports/shap_summary_bar.png`
- DL comparison: `reports/dl_experiments_comparison.png`
- Threshold curve: `reports/fig_threshold_curves.png`
- Confusion matrix: `reports/fig_confusion_matrix.png`
