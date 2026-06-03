# Pulsevera — Business Narrative & Impact Statement
> P1-4 · CC26-PRU439 · DBS Foundation Coding Camp 2026

---

## 1. Konteks & Relevansi: Mengapa Penyakit Jantung?

Penyakit kardiovaskular (CVD) adalah **pembunuh nomor satu di Indonesia** — dan dunia.

| Statistik | Data |
|---|---|
| Penyebab kematian #1 di Indonesia | Kemenkes RI 2023 |
| ~17% dari seluruh kematian di Indonesia | Riset Kesehatan Dasar (Riskesdas) 2023 |
| ~635.000 kematian/tahun di Indonesia | WHO Global Health Estimates 2023 |
| Serangan jantung pertama: **40% fatal** (sebelum sempat ke RS) | AHA Heart Disease and Stroke Statistics 2024 |
| Biaya perawatan CVD per pasien: Rp 30–150 juta/episode | BPJS Kesehatan Annual Report 2022 |
| Hanya **1 dari 3** penderita faktor risiko mengetahui kondisinya | Survei Biomedis Riskesdas 2019 |

**Masalah inti:** Penyakit jantung sangat *preventable* — tapi sebagian besar orang **tidak menyadari risiko mereka** sampai sudah terlambat.

---

## 2. Problem Definition: 3 Gap yang Pulsevera Isi

### Gap 1 — Akses Screening Terbatas
- Screening EKG/echocardiogram membutuhkan: peralatan khusus, tenaga medis terlatih, biaya Rp 300K–2,5 juta
- Hanya tersedia di RS tipe B/C ke atas; tidak ada di puskesmas kecamatan
- Di luar Jawa: rasio dokter jantung 1:1,2 juta penduduk (vs. standar WHO 1:100.000)

### Gap 2 — Kesadaran Rendah di Usia Produktif
- 68% kasus CVD fatal menyerang di **usia 40–64 tahun** — tapi faktor risiko mulai terbentuk di usia 20-an
- Generasi muda (25–34) cenderung merasa "terlalu muda" untuk khawatir tentang jantung
- Tidak ada titik sentuh edukasi yang **spesifik, personal, dan berbasis data** untuk mereka

### Gap 3 — Diagnosis ≠ Satu-Satunya Opsi
- Untuk deteksi dini, seseorang tidak harus terlebih dahulu pergi ke dokter
- **Awareness berbasis data** cukup untuk mengubah perilaku — bila disampaikan dengan cara yang tepat
- Kunci: personalisasi + transparansi hasil (bukan sekadar "Anda berisiko tinggi")

---

## 3. Solusi: Pulsevera

**Pulsevera** adalah aplikasi web berbasis AI yang memungkinkan siapa pun — tanpa latar belakang medis — untuk:
1. Menginput 10 pertanyaan tentang gaya hidup sehari-hari (< 2 menit)
2. Mendapatkan **Skor Gaya Hidup** (0–5) yang dipersonalisasi dan mudah dipahami
3. Menerima **Estimasi Risiko Serangan Jantung** berbasis model ML (probabilitas)
4. Membaca rekomendasi perubahan gaya hidup yang actionable

> **Pulsevera bukan pengganti dokter.** Pulsevera adalah *pintu masuk* — alat kesadaran yang mendorong orang untuk memulai perjalanan kesehatan jantung mereka.

---

## 4. Target User Persona

### Persona Utama: "Rafi" — Urban Professional Muda

| Atribut | Detail |
|---|---|
| **Usia** | 25–34 tahun |
| **Profil** | Pekerja kantoran di kota besar (Jakarta, Bandung, Surabaya) |
| **Gaya hidup** | Duduk 8+ jam/hari, jarang olahraga, merokok kadang-kadang, kurang tidur |
| **Digital literacy** | Smartphone-first, nyaman dengan web app |
| **Kesadaran kesehatan** | Rendah — "masih muda, belum perlu khawatir" |
| **Pain point** | Tidak tahu harus mulai dari mana, takut hasil buruk, tidak ada waktu ke dokter |
| **Motivasi** | Ingin tahu kondisi real-nya, tapi butuh pendekatan yang non-menghakimi |

### Persona Sekunder: "Sinta" — Keluarga dengan Riwayat CVD

| Atribut | Detail |
|---|---|
| **Usia** | 35–50 tahun |
| **Profil** | Orang tua atau anak dari pasien CVD, mencari tools preventif |
| **Motivasi** | Ada anggota keluarga yang pernah serangan jantung; ingin tahu risikonya sendiri |
| **Value** | Mau bayar untuk layanan yang memberikan insight bermakna |

---

## 5. Value Proposition

| Aspek | Tradisional (Klinik/RS) | Pulsevera |
|---|---|---|
| **Akses** | Perlu jadwal dokter, antrian, biaya | Langsung di browser, gratis, 24/7 |
| **Waktu** | 1–3 jam per kunjungan | < 2 menit |
| **Output** | Angka klinis (EKG, lipid panel) | Insight gaya hidup yang actionable |
| **Personalisasi** | Generik (form standar) | AI-generated rekomendasi per profil |
| **Bahasa** | Teknis medis | Bahasa awam yang mudah dipahami |
| **Follow-up** | Pasif (tunggu hasil lab) | Aktif (skor, rekomendasi, edukasi) |

---

## 6. Impact Metrics

### Dampak Langsung (Per User)
- Setiap user yang **mengetahui risiko tingginya** = 1 potensial kunjungan dokter yang dipercepat
- Setiap user dengan **skor gaya hidup rendah** yang memperbaiki 1 kebiasaan = penurunan risiko CVD 10–20% (berdasarkan meta-analisis AHA 2022)
- Setiap kampanye edukasi yang menjangkau 1.000 user = potensi 50–100 deteksi dini

### Dampak Jangka Panjang
- Jika **0,1% penduduk Indonesia usia 25–45** (sekitar 60 juta) menggunakan Pulsevera = 60.000 user
- Asumsi 5% terdeteksi risiko tinggi = **3.000 orang** yang potensial mendapat intervensi dini
- Biaya intervensi preventif vs. emergency CVD: **10–50x lebih murah**
- Potensi penghematan biaya kesehatan BPJS: miliaran rupiah/tahun

### Metrik Keberhasilan Aplikasi
| Metrik | Target (3 bulan) |
|---|---|
| Total screening dilakukan | 1.000+ |
| User berhasil selesaikan form (completion rate) | > 80% |
| User dengan Lifestyle Score < 3 mendapat rekomendasi | 100% (automated) |
| User yang kembali cek ulang (retention) | > 20% |

---

## 7. Kenapa Ini Bukan Sekadar "Chatbot Kesehatan"

Pulsevera berbeda dari health chatbot generik karena:

1. **Berbasis data epidemiologis nyata** — CDC BRFSS 2022 (445K responden survei kesehatan aktual)
2. **Model ML yang tervalidasi** — Acc 85.76%, Recall 71.15%, ROC-AUC 88.12%
3. **Explainability via SHAP** — output bisa dijelaskan secara ilmiah, bukan black box
4. **Dual-metric output** — Lifestyle Score (dapat diubah) + Risk Score (probabilitas statistik)
5. **Transparansi disclaimer** — bukan diagnosis, bukan pengganti dokter; disampaikan dengan jelas

---

## 8. Positioning & Roadmap

### Saat Ini (MVP — Live)
- Single-page app: screening → hasil → rekomendasi
- Tidak menyimpan data user (privasi by design)
- **Sudah live di production:**
  - Frontend: https://pulsevera.vercel.app
  - ML API: https://tgrrr-pulsevera-ml-api.hf.space
  - Backend: https://tgrrr-pulsevera-backend.hf.space
  - Source: https://github.com/muhamadtegar1/pulsevera-CC26-PRU439

### Short-term (3–6 bulan setelah capstone)
- History tracking (opsional, dengan consent)
- Halaman edukasi/news tentang CVD
- Dataset Indonesia untuk fine-tuning model

### Long-term Vision
- API untuk integrasi dengan sistem FKTP (Fasilitas Kesehatan Tingkat Pertama)
- Versi mobile app
- Kemitraan dengan BPJS/asuransi untuk program preventif

---

*Pulsevera — Karena jantungmu layak untuk tahu lebih awal.*  
*CC26-PRU439 · DBS Foundation Coding Camp 2026*
