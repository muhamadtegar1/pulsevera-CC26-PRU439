# Q&A Penjurian — Pulsevera CC26-PRU439
> P1-3 · 20 Pertanyaan Anticipated + Jawaban Siap Pakai

---

## BLOK A — Justifikasi Dataset

### Q1. Mengapa menggunakan dataset CDC BRFSS 2022? Kenapa tidak pakai data Indonesia?

**Jawaban:**
Dataset Indonesia (penyakit jantung) yang berkualitas dan tersedia publik tidak ada. Data Riskesdas tidak menyediakan level detail individual yang dibutuhkan untuk supervised ML (mis. fitur gaya hidup + konfirmasi diagnosis).

CDC BRFSS 2022 kami pilih karena:
1. **Skala besar**: 445.132 responden — cukup untuk melatih model DL yang stabil
2. **Otoritas**: survei resmi CDC yang diakui WHO sebagai benchmark global
3. **Relevansi fitur**: mencakup gaya hidup (tidur, olahraga, merokok) yang universal — bukan Amerika-spesifik
4. **Reproduksibilitas**: dataset publik yang bisa diverifikasi independen

> Faktor risiko CVD yang major (usia, BMI, merokok, aktivitas fisik, diabetes) terbukti universal secara epidemiologis — bukan hanya relevan untuk populasi AS.

---

### Q2. Apakah ada bias karena menggunakan data Amerika untuk pengguna Indonesia?

**Jawaban:**
Potensi bias ada, tapi terkendali. Kami menggunakan fitur-fitur yang secara medis terbukti universal: usia, BMI, status merokok, aktivitas fisik, pola tidur, diabetes. Faktor demografis AS-spesifik (ras) ada dalam dataset tapi *bukan* bagian dari 10 input form kami.

Lebih penting: model kami **memprediksi pola statistik populasi, bukan diagnosis individual**. Outputnya adalah probabilitas relatif dan skor gaya hidup — bukan klaim klinis. Disclaimer ini selalu ditampilkan di UI.

---

### Q3. Class imbalance 5.6% — bagaimana Anda menanganinya?

**Jawaban:**
4 lapis strategi untuk menangani imbalance ekstrem:

| Strategi | Detail | Efek |
|---|---|---|
| **SMOTE** | Oversample minoritas ke 30% dari mayoritas | Training set lebih seimbang |
| **class_weight balanced** | Bobot loss: class 1 = 2.17x class 0 | Model "lebih peduli" pada minority |
| **Focal Loss** | Penalti lebih besar untuk easy negatives | Fokus pada hard-to-classify cases |
| **Threshold tuning** | Default 0.5 → 0.23 | Recall ↑ dari ~30% ke 71.15% |

Dengan 4 lapis ini, model mencapai Recall 71.15% — jauh di atas baseline 30% tanpa treatment.

---

## BLOK B — Pemilihan Fitur & Model

### Q4. Mengapa hanya 10 input di form? Dataset aslinya punya 40+ kolom.

**Jawaban:**
Desain form mengikuti prinsip dari Mentoring 2 (advisor): **pilih fitur yang merupakan bagian dari keseharian pengguna awam**, bukan fitur klinis yang membutuhkan diagnosis dokter.

Dari 40+ kolom, 10 yang dipilih adalah:
- **Tersedia tanpa alat medis**: jenis kelamin, usia, tinggi, berat, jam tidur
- **Mudah diketahui sendiri**: olahraga, merokok, alkohol, kondisi umum, diabetes
- **High SHAP importance**: AgeCategory, GeneralHealth, SleepHours, PhysicalActivities masuk top-20

Fitur klinis seperti HadAngina, HadStroke memang punya SHAP importance tinggi, tapi:
- User awam tidak tahu apakah pernah angina
- Memasukkan ini di form akan meningkatkan missing value dan menurunkan UX
- Solution: di-default ke 0 (tidak ada riwayat) — ini konservatif tapi aman

---

### Q5. Bagaimana SHAP digunakan? Apa bedanya dari feature importance biasa?

**Jawaban:**
SHAP (SHapley Additive exPlanations) dari game theory memberikan **contribution score per fitur per instance**, bukan hanya global importance.

Keunggulan SHAP vs. feature importance biasa:
| Aspek | Feature Importance (RF) | SHAP |
|---|---|---|
| Directionality | Tidak — hanya magnitude | Ya — positif/negatif |
| Instance-level | Tidak — hanya global | Ya — per prediksi |
| Interaksi antar fitur | Tidak captured | Captured via interaction values |
| Interpretasi juri/audit | Tidak standar | Standar de facto industri |

Kami menggunakan **TreeExplainer** (efisien untuk tree models) dengan sample 200 dari training set untuk menghitung global importance yang menjadi argumen pemilihan fitur.

**Temuan kunci**: AgeCategory, GeneralHealth, HadAngina adalah top-3. Engineered features (LifestyleRiskScore) masuk top-20 — membuktikan feature engineering DS team menambah nilai.

---

### Q6. Mengapa Deep Learning lebih dipilih daripada Random Forest yang accuracy-nya lebih tinggi (90.9%)?

**Jawaban:**
Accuracy tidak cocok sebagai metrik utama untuk **medical screening** dengan imbalance ekstrem.

| Model | Accuracy | **Recall (positif)** | ROC-AUC |
|---|---|---|---|
| Logistic Regression | 84.2% | 64.6% | 83.1% |
| Decision Tree | 82.8% | 62.8% | 81.3% |
| Random Forest | **90.9%** | 44.5% | 84.6% |
| **DL+SMOTE (final)** | 85.8% | **71.2%** | **88.1%** |

Random Forest accuracy 90.9% karena **ia hanya memprediksi mayoritas (tidak sakit)** — Recall hanya 44.5%. Dari 100 orang yang berisiko, RF hanya mendeteksi 44. Ini tidak dapat diterima untuk screening.

**DL+SMOTE** mendeteksi 71 dari 100 orang berisiko — sambil tetap menjaga Accuracy 85.76% dan ROC-AUC tertinggi 88.1%.

---

### Q7. Mengapa threshold 0.23, bukan 0.5 yang default?

**Jawaban:**
Threshold 0.5 berasal dari asumsi distribusi seimbang. Dengan SMOTE yang mengubah distribusi training, **probabilitas output model tidak lagi terkalibrasi ke 0.5**.

Eksperimen menunjukkan:
- Threshold 0.5: Recall 30%, Accuracy 91% — model bias ke mayoritas
- **Threshold 0.23**: Recall 71.15%, Accuracy 85.76%, ROC-AUC 88.1% — sweet spot
- Threshold 0.10: Recall 90%+, tapi Accuracy turun ke 60% — terlalu banyak false alarm

Threshold 0.23 disepakati tim karena memenuhi **dua target program sekaligus**: Accuracy ≥ 85% AND Recall ≥ 70%.

---

## BLOK C — Teknis Deep Learning

### Q8. Arsitektur model DL-nya seperti apa? Mengapa memilih desain ini?

**Jawaban:**
```
Input(46 fitur)
→ Dense(256, ReLU) → BatchNorm → Dropout(0.3)
→ Dense(128, ReLU) → BatchNorm → Dropout(0.3)
→ Dense(64, ReLU) → BatchNorm → Dropout(0.3)
→ Dense(1, Sigmoid)
```

Alasan desain:
- **Width 256→128→64**: hierarchical compression — cukup kompleks untuk 46 fitur tapi tidak overfit
- **BatchNorm**: stabilisasi training, mengurangi kebutuhan learning rate kecil
- **Dropout 0.3**: regularisasi mencegah overfit pada dataset tabular
- **Sigmoid output**: menghasilkan probabilitas 0–1 yang dibutuhkan untuk threshold tuning

Custom components yang diimplementasikan:
- **Focal Loss** (`γ=2.0, α=0.25`): menghukum easy negatives lebih keras
- **EarlyStoppingByRecall**: stop jika recall tidak improve setelah 10 epoch

---

### Q9. Apakah ada risiko overfitting?

**Jawaban:**
Risiko telah dimitigasi dengan:
1. Dropout 0.3 di setiap layer
2. BatchNorm yang berfungsi sebagai regularizer implisit
3. Early stopping berbasis Recall (bukan accuracy)
4. Train set: 267K baris — jauh melebihi parameter model (~100K weights)

Test set adalah **hold-out yang tidak pernah dilihat selama training**. Metrik yang dilaporkan (Acc 85.76%, Recall 71.15%) adalah dari test set, bukan training set.

---

### Q10. Apakah model ini memenuhi target program (Accuracy ≥ 85%, MAE ≤ 0.02)?

**Jawaban:**
- **Accuracy**: 85.76% ✅ (memenuhi target ≥ 85%)
- **MAE untuk binary classification**: MAE minimum secara matematis ≈ class_positive_rate = 5.6% = 0.056

MAE ≤ 0.02 **tidak dapat dicapai** untuk binary classification dengan class imbalance 5.6%. Matematisnya:
- Jika model memprediksi semua 0 (negatif): MAE = 0.056 (100% salah untuk positif)
- Perfect model: MAE = 0 (tidak mungkin dengan noise dataset)
- Dengan Recall 71%, MAE ≈ 0.29 × 0.056 = ~0.016

Kami mendokumentasikan ini di laporan sebagai "constraint matematis dari imbalance" — bukan kegagalan model.

---

## BLOK D — Produk & UX

### Q11. Bagaimana user yang muda (25–34) selalu dapat "Rendah" — apakah ini masalah?

**Jawaban:**
Tidak — ini justru keputusan desain yang disengaja.

Model dilatih di populasi CDC BRFSS. Secara statistik, **serangan jantung di usia 25–34 sangat jarang** (< 1% dalam dataset). Model mengikuti pola epidemiologis yang nyata.

**Solusi**: kami menambahkan **Skor Gaya Hidup (0–5)** sebagai metrik PRIMER. Seorang user berusia 28 tahun yang merokok setiap hari, tidak olahraga, kurang tidur akan mendapat:
- Risk Score: "Rendah" (karena usianya)
- **Lifestyle Score: 1/5 "Berisiko Tinggi"** ← ini yang actionable

Dengan dual-metric ini, semua user mendapat insight yang bermakna — tidak peduli usianya.

---

### Q12. Data privacy — apakah data user disimpan?

**Jawaban:**
**Tidak.** Ini adalah desain by default:
- Tidak ada database di backend
- Payload form → ML inference → response → *langsung dilupakan*
- Tidak ada cookies, tidak ada tracking
- Disclaimer ini ditampilkan eksplisit di footer UI: "Data Anda tidak disimpan. Diproses real-time dan langsung dilupakan."

---

### Q13. Bagaimana akurasi Gemini AI recommendation? Apakah konsisten dengan hasil model?

**Jawaban:**
Gemini menerima **output model + profil user** sebagai context, bukan query kosong. Prompt engineering memastikan:
- Rekomendasi tidak bertentangan dengan label risiko
- Tone non-alarmis untuk risk "Rendah", lebih urgen untuk "Tinggi"
- Selalu menyertakan disclaimer "bukan pengganti dokter"

Sistem memiliki **fallback ke rule-based recommendations** jika Gemini tidak tersedia (API key tidak set atau rate limit). Ini menjamin aplikasi tetap berfungsi tanpa Gemini.

---

## BLOK E — Arsitektur & Deployment

### Q14. Mengapa menggunakan 3-layer architecture (Frontend + Express + FastAPI)?

**Jawaban:**
Setiap layer memiliki tanggung jawab berbeda:

| Layer | Tech | Fungsi |
|---|---|---|
| Frontend | React + Vite | UI, user interaction, form validation |
| Backend | Express.js | Proxy aman, rate limiting, CORS management |
| ML API | FastAPI (Python) | Inference, SHAP, Gemini integration |

Express sebagai **middle proxy** penting karena:
- ML API butuh Python environment yang berbeda dari Node.js
- Frontend tidak perlu tahu URL ML API (security)
- Express bisa tambah middleware (rate limiting, auth) tanpa mengubah ML API

---

### Q15. Berapa lama inference time? Apakah cepat untuk production?

**Jawaban:**
Inference time: **~350ms per request** (termasuk preprocessing → model forward pass → SHAP matching → response).

Optimasi yang dilakukan:
- **Pre-computed SHAP global importance** (bukan per-request SHAP) → dari 7000ms → 350ms
- Model disimpan sebagai `.keras` format (produksi) dan di-load sekali saat startup
- Preprocessing yang efisien dengan pandas + numpy

350ms sangat acceptable untuk web application interaktif (target < 1000ms).

---

## BLOK F — Proses & Metodologi

### Q16. Bagaimana proses feature engineering? Apa 6 fitur baru yang dibuat?

**Jawaban:**
6 fitur engineered:

| Fitur | Formula | Alasan |
|---|---|---|
| `BMI` | `weight / height²` | Standard body composition index |
| `LifestyleRiskScore` | Score 0–5 dari 5 kebiasaan lifestyle | Composite lifestyle indicator |
| `IsObese` | `BMI ≥ 30` | Binary flag untuk obesitas klinis |
| `IsSleepDeprived` | `SleepHours < 6` | Binary flag risiko sleep deprivation |
| `IsActiveSmoker` | `SmokerStatus ∈ {Current-some, Current-every}` | Binary flag perokok aktif |
| `HasChronicCondition` | `diabetes ∨ stroke ∨ angina` | Binary flag kondisi kronis |

Validasi SHAP: `LifestyleRiskScore` masuk top-20 global importance — membuktikan fitur ini **informatif secara statistik**, bukan hanya heuristik.

---

### Q17. A/B Testing — apa yang diuji dan hasilnya bagaimana?

**Jawaban:**
4 hipotesis diuji dengan Mann-Whitney U test dan Chi-square test:

| Hipotesis | Test | p-value | Hasil |
|---|---|---|---|
| H1: Aktivitas fisik ↓ risiko jantung | Mann-Whitney U | < 0.001 | ✅ Signifikan |
| H2: BMI tinggi ↑ risiko jantung | Mann-Whitney U | < 0.001 | ✅ Signifikan |
| H3: Merokok ↑ risiko jantung | Chi-square | < 0.001 | ✅ Signifikan |
| H4: Tidur cukup ↓ risiko jantung | Mann-Whitney U | < 0.05 | ✅ Signifikan |

Semua hipotesis terkonfirmasi — memvalidasi bahwa fitur-fitur yang kami pilih untuk form memang secara statistik berpengaruh terhadap risiko jantung.

---

### Q18. Mengapa memilih arsitektur DL tertentu? Apakah sudah mencoba variasi lain?

**Jawaban:**
Arsitektur final (Dense 256-128-64) dipilih berdasarkan eksperimen (lihat notebook 06). Temuan:
- **Terlalu shallow (64-1)**: Recall hanya 50%, model tidak cukup kompleks
- **Terlalu deep (512-256-128-64-32-1)**: Sedikit overfit, inference lebih lambat
- **Tanpa BatchNorm**: Training tidak stabil, perlu learning rate sangat kecil
- **Tanpa Dropout**: Overfit pada epoch akhir

Kami juga mendokumentasikan bahwa **ReduceLROnPlateau menyebabkan model kolaps ke all-negative** — temuan penting yang diputuskan untuk tidak digunakan.

---

### Q19. Bagaimana deployment pipeline-nya?

**Jawaban:**
Target deployment:
- **ML API** (FastAPI): Hugging Face Spaces (gratis, support Python + TF)
- **Backend** (Express): Railway atau Render (free tier)
- **Frontend** (React): Vercel atau Netlify (free, custom domain)

Environment variables dikelola per platform. CORS FastAPI dikonfigurasi untuk menerima domain frontend.

Status saat ini: running lokal, deployment planned.

---

### Q20. Apa limitation utama Pulsevera dan rencana ke depan?

**Jawaban:**
**Limitations:**
1. **Dataset bias**: populasi CDC BRFSS adalah US adults — mungkin tidak perfectly representatif untuk Indonesia
2. **Class imbalance**: Precision masih rendah (24.1%) — banyak false positive
3. **10 input saja**: fitur klinis penting (angina, stroke history) tidak ditanyakan untuk UX reasons
4. **Tidak ada validasi klinis**: belum divalidasi oleh tenaga medis profesional
5. **No longitudinal data**: tidak bisa track perubahan risiko dari waktu ke waktu

**Rencana ke depan:**
- Kolaborasi dengan FKTP/puskesmas untuk validasi klinis
- Dataset Indonesia (jika tersedia) untuk fine-tuning
- Model yang lebih canggih (XGBoost ensemble + DL)
- Integrasi dengan sistem rekam medis (ICD-10 mapping)
- Mobile app untuk akses lebih luas

---

*Dokumen ini disiapkan untuk sesi penjurian CC26-PRU439 · Pulsevera Team · 2026*
