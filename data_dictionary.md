# Data Dictionary - Pulsevera Capstone Project

**Dataset:** CDC BRFSS (Behavioral Risk Factor Surveillance System) 2022  
**Sumber:** Centers for Disease Control and Prevention (CDC), USA  
**Ukuran Original:** 445.132 baris × 40 kolom  
**Ukuran Final (dengan fitur baru):** 445.132 baris × 47 kolom  
**Target Variable:** `HadHeartAttack`

---

## Kolom Original

### Demografis

| Nama Kolom | Tipe | Deskripsi | Nilai Unik / Range | Missing % | Catatan |
|---|---|---|---|---|---|
| `Sex` | int | Jenis kelamin responden | 0=Perempuan, 1=Laki-laki | 0% | Encoded dari Male/Female |
| `AgeCategory` | int | Kategori usia (ordinal) | 1=18-24, 2=25-29, 3=30-34, 4=35-39, 5=40-44, 6=45-49, 7=50-54, 8=55-59, 9=60-64, 10=65-69, 11=70-74, 12=75-79, 13=80+ | 0% | Ordinal encoding dari string; interval 5 tahun dari usia 18-79, lalu semua usia 80+ digabung dalam satu bucket |
| `Race_Black only, Non-Hispanic` | uint8 | Ras: Kulit Hitam (non-Hispanik) | 0, 1 | 0% | One-hot dari RaceEthnicityCategory |
| `Race_Hispanic` | uint8 | Ras: Hispanik | 0, 1 | 0% | One-hot dari RaceEthnicityCategory |
| `Race_Multiracial, Non-Hispanic` | uint8 | Ras: Multirasial (non-Hispanik) | 0, 1 | 0% | One-hot dari RaceEthnicityCategory |
| `Race_Other race only, Non-Hispanic` | uint8 | Ras: Lainnya (non-Hispanik) | 0, 1 | 0% | One-hot dari RaceEthnicityCategory |
| `Race_White only, Non-Hispanic` | uint8 | Ras: Kulit Putih (non-Hispanik) | 0, 1 | 0% | One-hot dari RaceEthnicityCategory |

### Kondisi Kesehatan Umum

| Nama Kolom | Tipe | Deskripsi | Nilai Unik / Range | Missing % | Catatan |
|---|---|---|---|---|---|
| `GeneralHealth` | int | Kondisi kesehatan umum (self-reported) | 1=Poor, 2=Fair, 3=Good, 4=Very good, 5=Excellent | 0% | Ordinal encoding |
| `PhysicalHealthDays` | float | Hari fisik tidak sehat dalam 30 hari terakhir | 0–30 | 0% | Outlier di-cap dengan IQR |
| `MentalHealthDays` | float | Hari mental tidak sehat dalam 30 hari terakhir | 0–30 | 0% | Outlier di-cap dengan IQR |
| `LastCheckupTime` | int | Waktu terakhir checkup kesehatan | Kategorik ordinal | 0% | Label encoded |

### Gaya Hidup

| Nama Kolom | Tipe | Deskripsi | Nilai Unik / Range | Missing % | Catatan |
|---|---|---|---|---|---|
| `PhysicalActivities` | int | Melakukan aktivitas fisik selain pekerjaan | 0=Tidak, 1=Ya | 0% | Encoded dari Yes/No |
| `SleepHours` | float | Rata-rata jam tidur per malam | 1–14 (setelah capping) | 0% | Outlier di-cap dengan IQR |
| `SmokerStatus` | float | Status merokok | 0=Never, 1=Former, 2=Some days, 3=Every day | 8.0% | Missing diisi modus; ordinal |
| `ECigaretteUsage` | float | Penggunaan rokok elektrik | 0=Never, 1=Not now, 2=Some days, 3=Every day | 0% | Ordinal encoding |
| `AlcoholDrinkers` | int | Konsumsi alkohol | 0=Tidak, 1=Ya | 0% | Encoded dari Yes/No |

### Indikator Berat Badan

| Nama Kolom | Tipe | Deskripsi | Nilai Unik / Range | Missing % | Catatan |
|---|---|---|---|---|---|
| `BMI` | float | Body Mass Index | 13–60 (setelah capping) | 0% | Outlier di-cap; 11% missing awal diisi median |
| `WeightInKilograms` | float | Berat badan dalam kilogram | Numerik | 0% | - |
| `HeightInMeters` | float | Tinggi badan dalam meter | Numerik | 0% | - |

### Target Variable & Riwayat Kardiovaskular

| Nama Kolom | Tipe | Deskripsi | Nilai Unik / Range | Missing % | Catatan |
|---|---|---|---|---|---|
| `HadHeartAttack` | int | **TARGET** – Pernah serangan jantung | 0=Tidak, 1=Ya | 0% | Class imbalance: ~5.6% positif |
| `HadAngina` | int | Pernah angina/nyeri dada | 0=Tidak, 1=Ya | 0% | Encoded dari Yes/No |
| `HadStroke` | int | Pernah stroke | 0=Tidak, 1=Ya | 0% | Encoded dari Yes/No |

### Riwayat Penyakit Kronis

| Nama Kolom | Tipe | Deskripsi | Nilai Unik / Range | Missing % | Catatan |
|---|---|---|---|---|---|
| `HadDiabetes` | float | Riwayat diabetes | 0=Tidak, 1=Pre-diabetes, 2=Gestasional, 3=Ya | 0% | Ordinal encoding |
| `HadAsthma` | int | Riwayat asma | 0=Tidak, 1=Ya | 0% | - |
| `HadCOPD` | int | Riwayat PPOK/penyakit paru kronis | 0=Tidak, 1=Ya | 0% | - |
| `HadKidneyDisease` | int | Riwayat penyakit ginjal | 0=Tidak, 1=Ya | 0% | - |
| `HadArthritis` | int | Riwayat artritis | 0=Tidak, 1=Ya | 0% | - |
| `HadSkinCancer` | int | Riwayat kanker kulit | 0=Tidak, 1=Ya | 0% | - |
| `HadDepressiveDisorder` | int | Riwayat gangguan depresi | 0=Tidak, 1=Ya | 0% | - |

### Disabilitas & Keterbatasan Fungsional

| Nama Kolom | Tipe | Deskripsi | Nilai Unik / Range | Missing % | Catatan |
|---|---|---|---|---|---|
| `DeafOrHardOfHearing` | int | Gangguan pendengaran | 0=Tidak, 1=Ya | 0% | - |
| `BlindOrVisionDifficulty` | int | Gangguan penglihatan | 0=Tidak, 1=Ya | 0% | - |
| `DifficultyConcentrating` | int | Kesulitan berkonsentrasi | 0=Tidak, 1=Ya | 0% | - |
| `DifficultyWalking` | int | Kesulitan berjalan | 0=Tidak, 1=Ya | 0% | - |
| `DifficultyDressingBathing` | int | Kesulitan berpakaian/mandi | 0=Tidak, 1=Ya | 0% | - |
| `DifficultyErrands` | int | Kesulitan mengurus keperluan sendiri | 0=Tidak, 1=Ya | 0% | - |

### Pencegahan & Pemeriksaan Kesehatan

| Nama Kolom | Tipe | Deskripsi | Nilai Unik / Range | Missing % | Catatan |
|---|---|---|---|---|---|
| `ChestScan` | int | Pernah melakukan CT scan dada | 0=Tidak, 1=Ya | 0% | - |
| `FluVaxLast12` | int | Vaksin flu dalam 12 bulan terakhir | 0=Tidak, 1=Ya | 0% | - |
| `HIVTesting` | int | Pernah tes HIV | 0=Tidak, 1=Ya | 0% | 14.9% missing awal; diisi modus |
| `CovidPos` | int | Pernah positif COVID-19 | 0=Tidak, 1=Ya | 0% | 11.4% missing awal; diisi modus |
| `HighRiskLastYear` | int | Perilaku berisiko tinggi dalam setahun terakhir | 0=Tidak, 1=Ya | 0% | 11.4% missing awal; diisi modus |
| `RemovedTeeth` | int | Pernah gigi dicabut | Kategorik ordinal | 0% | Label encoded |

---

## Kolom Dihapus (Drop)

| Nama Kolom | Alasan Drop |
|---|---|
| `TetanusLast10Tdap` | Missing 18.5% > threshold 15%; tidak relevan langsung dengan risiko jantung |
| `PneumoVaxEver` | Missing 17.3% > threshold 15%; tidak relevan langsung dengan risiko jantung |
| `State` | 54 kategori unik (negara bagian USA), tidak relevan untuk prediksi individu |
| `RaceEthnicityCategory` | Di-replace dengan one-hot encoding |

---

## Fitur Baru (Feature Engineering)

| Nama Kolom | Tipe | Deskripsi | Nilai Unik / Range | Missing % | Catatan |
|---|---|---|---|---|---|
| `IsActiveSmoker` | int | Perokok aktif saat ini | 0=Tidak, 1=Ya | 0% | Derived: SmokerStatus >= 2 |
| `IsObese` | int | Indikator obesitas | 0=Tidak, 1=Ya | 0% | Derived: BMI >= 30 |
| `IsSleepDeprived` | int | Kurang tidur (di bawah rekomendasi WHO) | 0=Tidak, 1=Ya | 0% | Derived: SleepHours < 6 |
| `LifestyleRiskScore` | int | Skor risiko gaya hidup gabungan | 0–5 | 0% | Sum: IsActiveSmoker + PhysInaktif + AlcoholDrinkers + IsSleepDeprived + IsObese |
| `HasChronicCondition` | int | Memiliki ≥1 penyakit kronis | 0=Tidak, 1=Ya | 0% | OR dari: Diabetes, Stroke, Asthma, COPD, KidneyDisease |
| `PoorHealthDays_Total` | float | Total hari tidak sehat (fisik + mental) | 0–60 | 0% | Sum: PhysicalHealthDays + MentalHealthDays |

---

## Catatan Penting

1. **Class Imbalance:** Target variable `HadHeartAttack` sangat tidak seimbang (~5.64% positif). AI Engineer harus menangani ini dengan SMOTE, class weighting, atau teknik resampling lainnya.
2. **Populasi:** Data berasal dari survei masyarakat **Amerika Serikat**. Hati-hati dalam generalisasi ke populasi Indonesia.
3. **Skala Data:** Semua kolom kategorik telah di-encode ke numerik. Encoding mapping tersimpan dalam notebook `01_data_wrangling.ipynb`.
4. **Outlier:** Outlier pada kolom numerik (BMI, SleepHours, PhysicalHealthDays, MentalHealthDays) telah di-cap menggunakan metode IQR (bukan dihapus).
5. **Target Variable:** Tim menggunakan `HadHeartAttack` sebagai target tunggal. Jika ingin menggunakan target komposit dengan `HadAngina`, perlu rerun pipeline dari awal.
6. **Data Split:** 80% training (356.105 baris), 20% testing (89.027 baris) dengan stratified split menjaga proporsi class.

---

*Terakhir diperbarui: 2026-05-06 | CC26-PRU439 Pulsevera*
