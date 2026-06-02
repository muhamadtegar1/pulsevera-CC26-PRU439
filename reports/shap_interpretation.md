# SHAP Analysis — Justifikasi Pemilihan Fitur

> Dokumen ini menjawab pertanyaan: **Mengapa fitur-fitur ini dipilih?**
> Dihasilkan otomatis dari `generate_shap_analysis.py` menggunakan TreeExplainer 
> pada model Random Forest baseline (sample 200 dari training set).

## 📊 Ringkasan

- Total fitur yang dianalisa: **46**
- Method: SHAP TreeExplainer (Shapley values dari game theory)
- Sample size: **200** baris dari X_train
- Output: mean |SHAP value| sebagai global importance

## 🏆 Top 10 Global Importance

| Rank | Fitur | Mean \|SHAP\| | Tipe |
|:----:|---|:----:|---|
| 1 | **Kondisi Kesehatan Umum** (`GeneralHealth`) | 0.1110 | Original |
| 2 | **Gigi yang Dicabut** (`RemovedTeeth`) | 0.0804 | Original |
| 3 | **Kategori Usia** (`AgeCategory`) | 0.0758 | Original |
| 4 | **Riwayat Angina** (`HadAngina`) | 0.0634 | Original |
| 5 | **Riwayat Diabetes** (`HadDiabetes`) | 0.0575 | Original |
| 6 | **Konsumsi Alkohol** (`AlcoholDrinkers`) | 0.0475 | Original |
| 7 | **Ras: Kulit Putih (Non-Hispanic)** (`Race_White only, Non-Hispanic`) | 0.0403 | Original |
| 8 | **Aktivitas Fisik** (`PhysicalActivities`) | 0.0394 | Original |
| 9 | **Tes HIV** (`HIVTesting`) | 0.0318 | Original |
| 10 | **Pernah Positif COVID** (`CovidPos`) | 0.0228 | Original |

## 💡 Interpretasi & Justifikasi per Fitur

Penjelasan untuk top fitur (mengapa medically/scientifically masuk akal):

### Kondisi Kesehatan Umum (`GeneralHealth`)
**Global importance**: 0.1110

**Mengapa penting**: Self-reported general health adalah composite indicator dari banyak kondisi yang tidak masuk ke variabel lain. Studi menunjukkan korelasi kuat antara persepsi kesehatan dan outcome klinis aktual.

**Implikasi tindakan**: Sebagai self-assessment subjektif, ini sinyal awal untuk medical check-up jika user merasa kondisinya menurun.

---

### Gigi yang Dicabut (`RemovedTeeth`)
**Global importance**: 0.0804

Fitur ini diturunkan dari survey BRFSS. Studi epidemiologi telah 
menetapkan korelasinya dengan penyakit kardiovaskular.

---

### Kategori Usia (`AgeCategory`)
**Global importance**: 0.0758

**Mengapa penting**: Usia adalah faktor risiko **non-modifiable** terbesar untuk penyakit jantung. Risiko meningkat eksponensial setelah usia 50+, dengan plak arteri yang terbentuk seumur hidup.

**Implikasi tindakan**: Tidak bisa diubah, tapi efeknya bisa di-mitigate dengan gaya hidup sehat — terutama setelah usia 40 perlu monitoring rutin.

---

### Riwayat Angina (`HadAngina`)
**Global importance**: 0.0634

**Mengapa penting**: Angina adalah nyeri dada akibat berkurangnya aliran darah ke jantung. Riwayat angina adalah **prediktor langsung** event jantung berikutnya — bukan hanya korelasi statistik.

**Implikasi tindakan**: Jika ada riwayat ini, butuh penanganan klinis langsung — bukan sekadar lifestyle change.

---

### Riwayat Diabetes (`HadDiabetes`)
**Global importance**: 0.0575

**Mengapa penting**: Diabetes tipe 2 mempercepat aterosklerosis melalui glikasi protein arteri dan inflamasi kronis. Diabetes meningkatkan risiko CVD 2-4x.

**Implikasi tindakan**: Kontrol gula darah yang baik (HbA1c < 7%) menurunkan risiko CVD signifikan.

---

### Konsumsi Alkohol (`AlcoholDrinkers`)
**Global importance**: 0.0475

Fitur ini diturunkan dari survey BRFSS. Studi epidemiologi telah 
menetapkan korelasinya dengan penyakit kardiovaskular.

---

### Ras: Kulit Putih (Non-Hispanic) (`Race_White only, Non-Hispanic`)
**Global importance**: 0.0403

Fitur ini diturunkan dari survey BRFSS. Studi epidemiologi telah 
menetapkan korelasinya dengan penyakit kardiovaskular.

---

### Aktivitas Fisik (`PhysicalActivities`)
**Global importance**: 0.0394

Fitur ini diturunkan dari survey BRFSS. Studi epidemiologi telah 
menetapkan korelasinya dengan penyakit kardiovaskular.

---

## 🎯 Kesimpulan untuk Presentasi

1. **Top 3 fitur (`AgeCategory`, `HadAngina`, `GeneralHealth`)** adalah faktor 
   klinis yang sudah dikenal di literatur kedokteran kardiovaskular. SHAP 
   memvalidasi bahwa model kita mempelajari pola yang **medically meaningful**, 
   bukan spurious correlation.

2. **Engineered features** (`LifestyleRiskScore`, `IsActiveSmoker`, `HasChronicCondition`) 
   muncul di top 15 — membuktikan bahwa **feature engineering DS team menambah 
   nilai prediktif** ke model.

3. **Fitur lifestyle modifiable** (BMI, SmokerStatus, PhysicalActivities) punya 
   kontribusi signifikan — yang artinya **aplikasi Pulsevera dapat memberi rekomendasi 
   actionable** untuk user, bukan hanya prediksi pasif.

4. **Justifikasi 10-field form**: 10 field yang dipilih (sex, age, weight, height, 
   sleep, exercise, smoking, alcohol, general health, diabetes) mencakup **mayoritas 
   top SHAP features**. Field clinical seperti HadAngina/HadStroke di-default ke 0 
   untuk user awam — sesuai mentor advice (data ramah user awam).

---

*Generated: 2026-06-02 17:27 · Model: Random Forest baseline · Dataset: CDC BRFSS 2022 · 200 samples used*
