# Pulsevera — Predict, Prevent, Prevail
**Coding Camp 2026 powered by DBS Foundation | CC26-PRU439**

> Sistem prediksi risiko penyakit jantung berbasis gaya hidup menggunakan machine learning, diakses melalui aplikasi web.

---

## Tim

| Nama | Role | Status |
|---|---|---|
| Muh. Tegar Adyaksa | Data Scientist | Aktif |
| Afifah Nurazizah | Data Scientist | Tidak Aktif |
| Fathan Rasyidi Mustafa | AI Engineer | Aktif |
| Shafira Kurnia Fasya | AI Engineer | Aktif |
| Muhammad Rifqi Indria Nugraha | Full-Stack Web Developer | Aktif |
| Khoerunnisa | Full-Stack Web Developer | Tidak Aktif |

---

## Dataset

Dataset **tidak disertakan di repository ini** karena ukurannya besar (>100MB).

**Download dataset di sini:**
> 📁 [Google Drive - Pulsevera Data](https://drive.google.com/drive/folders/1jtkudb-Ggt4nk9gZygS4O87hWGDT0sbH?usp=sharing)

Setelah download, letakkan file sesuai struktur berikut:
```
pulsevera-cc26-pru439/
└── data/
    ├── raw/dataset_raw.csv
    ├── processed/dataset_cleaned.csv
    └── final/
        ├── X_train.csv        (356.105 baris × 46 fitur)
        ├── X_test.csv         (89.027 baris × 46 fitur)
        ├── y_train.csv
        ├── y_test.csv
        └── dataset_final.csv
```

---

## Struktur Repository

```
pulsevera-cc26-pru439/
├── notebooks/
│   ├── 01_data_wrangling.ipynb       ← [DS]  Data Gathering, Assessing, Cleaning
│   ├── 02_eda.ipynb                  ← [DS]  EDA + 5 Business Questions
│   ├── 03_feature_engineering.ipynb  ← [DS]  6 Fitur Baru + Train-Test Split
│   ├── 04_ab_testing.ipynb           ← [DS]  4 Hipotesis A/B Testing
│   ├── 05_ml_modeling.ipynb          ← [AI]  LR + RF + DT + SMOTE + tuning
│   ├── 06_deep_learning.ipynb        ← [AI]  TF Functional API + Focal Loss + Custom Callback
│   ├── 07_evaluation_shap.ipynb      ← [AI]  Evaluasi komprehensif + SHAP + demo inference
│   └── figures/                      ← Visualisasi PNG (DS + AI)
├── dashboard/
│   └── app.py                        ← [DS]  Streamlit Dashboard
├── ml-api/                           ← [AI]  FastAPI inference API
│   ├── main.py                       ←       FastAPI app + endpoints + Gemini AI
│   ├── preprocessing.py              ←       10 field → 46 fitur
│   ├── inference.py                  ←       Model loading + SHAP + recommendations
│   ├── train.py                      ←       Standalone training pipeline
│   ├── requirements.txt
│   ├── .env.example                  ←       Setup Gemini API key
│   ├── README.md                     ←       Dokumentasi detail ml-api
│   └── models/                       ←       .pkl / .keras / metadata (gitignored)
├── backend/                          ← [Full-Stack] Node.js/Express (proxy)
│   ├── server.js
│   ├── src/
│   │   ├── app.js
│   │   ├── controllers/predictController.js
│   │   └── routes/predictRoutes.js
│   └── package.json
├── frontend/                         ← [Full-Stack] React + Vite + Tailwind
│   ├── src/
│   │   ├── App.jsx                   ←       react-router (/, /check-risk, /result)
│   │   ├── pages/                    ←       Landing, Form (multi-step), Result
│   │   ├── sections/                 ←       Hero, Stats, Features, How, About, FAQ, CTA
│   │   ├── components/               ←       Navbar, Footer, RiskGauge, 3D scenes
│   │   └── services/api.js
│   └── package.json
└── data_dictionary.md                ← Dokumentasi lengkap 47 kolom
```

---

## Quick Start

### Streamlit Dashboard (Data Science)
```bash
pip install streamlit plotly pandas scikit-learn scipy
streamlit run dashboard/app.py
```

### Jupyter Notebooks
```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn plotly imbalanced-learn joblib tensorflow shap
jupyter notebook notebooks/
```

### ML API (FastAPI — AI Engineer)
```bash
cd ml-api
pip install -r requirements.txt
cp .env.example .env          # isi GEMINI_API_KEY (opsional)
python train.py               # latih ML + DL + SHAP (butuh data/final/)
uvicorn main:app --reload --port 8000
```
Buka `http://localhost:8000/docs` untuk dokumentasi interaktif. Detail di [`ml-api/README.md`](ml-api/README.md).

### Backend (Express — proxy ke ML API)
```bash
cd backend
cp .env.example .env          # PORT=3001, ML_API_URL=http://localhost:8000
npm install
npm run dev                   # http://localhost:3001
```

### Frontend (React + Vite)
```bash
cd frontend
cp .env.example .env          # VITE_API_URL=http://localhost:3001
npm install
npm run dev                   # http://localhost:5173
```

---

## Progress

### Data Science ✅ Selesai
- [x] Data Gathering & Wrangling (`01_data_wrangling.ipynb`)
- [x] EDA — 5 pertanyaan bisnis, 13 visualisasi (`02_eda.ipynb`)
- [x] Feature Engineering — 6 fitur baru (`03_feature_engineering.ipynb`)
- [x] A/B Testing — 4 hipotesis (`04_ab_testing.ipynb`)
- [x] Dashboard Streamlit (`dashboard/app.py`)
- [x] Data siap untuk model (`data/final/`)
- [x] Data Dictionary (`data_dictionary.md`)
- [ ] Laporan Teknis PDF

### AI Engineer ✅ Selesai (kontribusi Fathan + Shafira)
- [x] Training ML models (LR, RF, DT) + SMOTE + class_weight (`05_ml_modeling.ipynb`)
- [x] Hyperparameter tuning (`RandomizedSearchCV`, scoring=`f1`)
- [x] Deep Learning — TensorFlow Functional API + Focal Loss + EarlyStoppingByRecall (`06_deep_learning.ipynb`)
- [x] SHAP interpretability — TreeExplainer / LinearExplainer (`07_evaluation_shap.ipynb`)
- [x] FastAPI endpoints: `/api/v1/predict` + `/api/v1/predict-dl` + `/api/v1/metadata` (`ml-api/main.py`)
- [x] Preprocessing pipeline 10 → 46 fitur (`ml-api/preprocessing.py`)
- [x] Generative AI recommendation via **Gemini API** (`ml-api/main.py`) — fallback rule-based
- [x] Standalone training pipeline (`ml-api/train.py`) + TensorBoard logging

### Full-Stack 🔄 Sebagian (kontribusi Rifqi + Shafira)
- [x] Frontend React (Vite + Tailwind + framer-motion + lucide-react + three.js)
- [x] Routing dengan `react-router-dom` (`/`, `/check-risk`, `/result`)
- [x] Landing page 7 sections + multi-step Form wizard + Result page interaktif
- [x] Backend Express terstruktur (`src/app.js`, `src/controllers/`, `src/routes/`)
- [x] Backend proxy ke ML API dengan validasi field & error handling
- [ ] Integrasi end-to-end (test setelah model dilatih)
- [ ] Mockup Figma
- [ ] Deployment (Netlify/Vercel + Railway/Render)

---

---

# Jobdesk: AI Engineer

**Anggota:** Fathan Rasyidi Mustafa & Shafira Kurnia Fasya

## Output Data Science yang Tersedia

| File | Lokasi | Keterangan |
|---|---|---|
| `X_train.csv` | `data/final/` | 356.105 baris × 46 fitur — siap training |
| `X_test.csv` | `data/final/` | 89.027 baris × 46 fitur — untuk evaluasi |
| `y_train.csv` | `data/final/` | Label training (0/1) |
| `y_test.csv` | `data/final/` | Label test (0/1) |
| `dataset_final.csv` | `data/final/` | Dataset lengkap + 6 fitur baru |
| `data_dictionary.md` | root | Deskripsi 47 kolom + encoding mapping |

**Catatan kritis:**
- Target: `HadHeartAttack` (binary: 0=Tidak, 1=Ya)
- **Class imbalance parah:** hanya **5.64%** kelas positif — wajib ditangani
- Fitur paling berkorelasi: `AgeCategory`, `HadAngina`, `HadStroke`, `GeneralHealth`, `HadDiabetes`, `LifestyleRiskScore`
- Semua encoding detail ada di `data_dictionary.md` dan `notebooks/01_data_wrangling.ipynb`

---

## Fase 1 — Machine Learning Models (Minggu 2–3)

### Setup Environment
```bash
pip install scikit-learn imbalanced-learn shap fastapi uvicorn joblib tensorflow
```

### Tangani Class Imbalance (Wajib sebelum training)
```python
from imblearn.over_sampling import SMOTE

# Opsi A — SMOTE (direkomendasikan)
smote = SMOTE(random_state=42, sampling_strategy=0.3)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# Opsi B — Class weighting (lebih ringan, cocok baseline cepat)
# LogisticRegression(class_weight='balanced')

# JANGAN apply SMOTE ke test set — biarkan X_test tetap asli
```

### Baseline Models
```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, roc_auc_score

models = {
    'Logistic Regression': LogisticRegression(class_weight='balanced', max_iter=1000),
    'Random Forest':       RandomForestClassifier(class_weight='balanced', random_state=42),
    'Decision Tree':       DecisionTreeClassifier(class_weight='balanced', random_state=42),
}

for name, model in models.items():
    model.fit(X_train_res, y_train_res)
    y_pred = model.predict(X_test)
    print(f"\n=== {name} ===")
    print(classification_report(y_test, y_pred))
    print(f"ROC-AUC: {roc_auc_score(y_test, model.predict_proba(X_test)[:,1]):.4f}")
```

### Hyperparameter Tuning
```python
from sklearn.model_selection import RandomizedSearchCV

param_grid_rf = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10],
    'class_weight': ['balanced', 'balanced_subsample']
}
rf_tuned = RandomizedSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid_rf, n_iter=20, cv=5,
    scoring='f1',        # pakai F1, BUKAN accuracy
    random_state=42, n_jobs=-1
)
rf_tuned.fit(X_train_res, y_train_res)
```

### Target Metrik Evaluasi

| Metrik | Minimum | Catatan |
|---|---|---|
| **Recall (kelas 1)** | ≥ 70% | Prioritas utama — jangan sampai kasus risiko tinggi terlewat |
| **F1-Score (kelas 1)** | ≥ 65% | Keseimbangan precision-recall |
| **ROC-AUC** | ≥ 0.80 | Kemampuan diskriminasi model |
| Accuracy | ≥ 85% | Sesuai requirement program (mudah tercapai karena 94% kelas negatif) |

### SHAP untuk Interpretabilitas
```python
import shap

def get_top_risk_factors(model, input_df, feature_names, top_n=3):
    """Kembalikan top N fitur paling berkontribusi pada prediksi."""
    explainer = shap.TreeExplainer(model)
    shap_vals = explainer.shap_values(input_df)[1]   # index 1 = kelas positif
    factors = pd.Series(shap_vals[0], index=feature_names)
    return factors.abs().nlargest(top_n).index.tolist()
```

---

## Fase 2 — Deep Learning (Minggu 3–4)

### Struktur Model (TensorFlow Functional API — Wajib)
```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def build_heart_disease_model(input_dim, dropout_rate=0.3):
    """Model klasifikasi risiko penyakit jantung — Functional API."""
    inputs = keras.Input(shape=(input_dim,), name='input_layer')
    x = layers.Dense(256, activation='relu')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(dropout_rate)(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(dropout_rate)(x)
    x = layers.Dense(64, activation='relu')(x)
    x = layers.Dropout(dropout_rate / 2)(x)
    outputs = layers.Dense(1, activation='sigmoid', name='output')(x)
    return keras.Model(inputs=inputs, outputs=outputs, name='pulsevera_model')
```

### Komponen Kustom — Pilih Minimal 1

**Opsi A — Custom Callback:**
```python
class EarlyStoppingByRecall(keras.callbacks.Callback):
    """Stop training jika recall kelas positif tidak naik."""
    def __init__(self, patience=5):
        super().__init__()
        self.patience = patience
        self.wait = 0
        self.best_recall = 0

    def on_epoch_end(self, epoch, logs=None):
        val_recall = logs.get('val_recall', 0)
        if val_recall > self.best_recall:
            self.best_recall = val_recall
            self.wait = 0
        else:
            self.wait += 1
            if self.wait >= self.patience:
                self.model.stop_training = True
```

**Opsi B — Custom Loss (Focal Loss untuk class imbalance):**
```python
def focal_loss(gamma=2.0, alpha=0.25):
    """Focal loss — lebih fokus ke kasus positif yang sulit diprediksi."""
    def loss(y_true, y_pred):
        bce = tf.keras.losses.binary_crossentropy(y_true, y_pred)
        p_t = tf.exp(-bce)
        return tf.reduce_mean(alpha * tf.pow(1 - p_t, gamma) * bce)
    return loss
```

### Training
```python
from sklearn.utils.class_weight import compute_class_weight

cw = compute_class_weight('balanced', classes=np.array([0, 1]), y=y_train.values)
class_weight_dict = {0: cw[0], 1: cw[1]}

model = build_heart_disease_model(input_dim=X_train.shape[1])
model.compile(
    optimizer=keras.optimizers.Adam(1e-3),
    loss=focal_loss(),
    metrics=['accuracy', keras.metrics.Recall(name='recall'), keras.metrics.AUC(name='auc')]
)
model.fit(X_train, y_train, epochs=50, batch_size=512,
          validation_split=0.2, class_weight=class_weight_dict,
          callbacks=[EarlyStoppingByRecall(patience=5)])
```

### Simpan Model (Format Produksi — Wajib)
```python
model.save('ml-api/models/pulsevera_dl_model.keras')   # Deep Learning
joblib.dump(best_ml_model, 'ml-api/models/pulsevera_ml_model.pkl')  # ML
```

---

## Fase 3 — Preprocessing Pipeline & FastAPI (Minggu 3–4)

User hanya mengisi 10 field (lihat bagian Full-Stack). AI Engineer harus konversi ke 46 fitur model:

```python
DEFAULT_VALUES = {
    'PhysicalHealthDays': 3.0, 'MentalHealthDays': 3.0,
    'HadAngina': 0, 'HadStroke': 0, 'HadAsthma': 0, 'HadCOPD': 0,
    'HadKidneyDisease': 0, 'HadArthritis': 0, 'HadSkinCancer': 0,
    'HadDepressiveDisorder': 0, 'DeafOrHardOfHearing': 0,
    'BlindOrVisionDifficulty': 0, 'DifficultyConcentrating': 0,
    'DifficultyWalking': 0, 'DifficultyDressingBathing': 0,
    'DifficultyErrands': 0, 'ChestScan': 0, 'HIVTesting': 0,
    'FluVaxLast12': 1, 'CovidPos': 0, 'HighRiskLastYear': 0,
    'LastCheckupTime': 1, 'RemovedTeeth': 0, 'ECigaretteUsage': 0,
    'Race_Black only, Non-Hispanic': 0, 'Race_Hispanic': 0,
    'Race_Multiracial, Non-Hispanic': 0,
    'Race_Other race only, Non-Hispanic': 0,
    'Race_White only, Non-Hispanic': 1,
}

def preprocess_user_input(user_input: dict) -> pd.DataFrame:
    """Konversi 10 field input user ke 46 fitur model."""
    data = DEFAULT_VALUES.copy()
    data['Sex'] = 1 if user_input['sex'] == 'Male' else 0
    data['AgeCategory'] = int(user_input['age_category'])
    height = user_input['height_meters']
    weight = user_input['weight_kg']
    data['BMI'] = weight / (height ** 2)
    data['WeightInKilograms'] = weight
    data['HeightInMeters'] = height
    data['SleepHours'] = float(user_input['sleep_hours'])
    data['PhysicalActivities'] = 1 if user_input['physical_activities'] == 'Yes' else 0
    data['AlcoholDrinkers'] = 1 if user_input['alcohol'] == 'Yes' else 0
    data['SmokerStatus'] = {'Never': 0, 'Former': 1, 'Current-some': 2, 'Current-every': 3}.get(user_input['smoker_status'], 0)
    data['GeneralHealth'] = {'Poor': 1, 'Fair': 2, 'Good': 3, 'Very good': 4, 'Excellent': 5}.get(user_input['general_health'], 3)
    data['HadDiabetes'] = {'No': 0, 'Pre-diabetes': 1, 'Yes': 3}.get(user_input.get('diabetes', 'No'), 0)
    # Feature engineering — harus konsisten dengan pipeline DS
    data['IsActiveSmoker'] = 1 if data['SmokerStatus'] >= 2 else 0
    data['IsObese'] = 1 if data['BMI'] >= 30 else 0
    data['IsSleepDeprived'] = 1 if data['SleepHours'] < 6 else 0
    data['LifestyleRiskScore'] = (data['IsActiveSmoker'] + (1 - data['PhysicalActivities']) +
                                   data['AlcoholDrinkers'] + data['IsSleepDeprived'] + data['IsObese'])
    data['HasChronicCondition'] = 1 if any(data[c] > 0 for c in ['HadDiabetes','HadStroke','HadAsthma','HadCOPD','HadKidneyDisease']) else 0
    data['PoorHealthDays_Total'] = data['PhysicalHealthDays'] + data['MentalHealthDays']
    return pd.DataFrame([data])[FEATURE_ORDER]   # FEATURE_ORDER = urutan kolom X_train
```

### FastAPI Endpoint
```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Pulsevera ML API", version="1.0")

class UserInput(BaseModel):
    sex: str
    age_category: int
    height_meters: float
    weight_kg: float
    sleep_hours: float
    physical_activities: str
    smoker_status: str
    alcohol: str
    general_health: str
    diabetes: Optional[str] = 'No'

class PredictionResult(BaseModel):
    risk_score: float      # probabilitas 0.0–1.0
    risk_label: str        # "Rendah" / "Sedang" / "Tinggi"
    top_risk_factors: list # ["AgeCategory", "BMI", "SmokerStatus"]
    recommendations: list  # ["Kurangi merokok", ...]

@app.post("/api/v1/predict", response_model=PredictionResult)
async def predict(user_input: UserInput):
    input_df = preprocess_user_input(user_input.dict())
    prob = ml_model.predict_proba(input_df)[0][1]
    label = "Rendah" if prob < 0.3 else "Sedang" if prob < 0.6 else "Tinggi"
    top_factors = get_top_risk_factors(ml_model, input_df, FEATURE_ORDER)
    return PredictionResult(risk_score=round(float(prob), 4), risk_label=label,
                            top_risk_factors=top_factors, recommendations=[])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
```

## Checklist AI Engineer

**Main Quest (Wajib)**
- [ ] ML models dilatih — min. 3 algoritma (LR, RF, DT)
- [ ] Class imbalance ditangani (SMOTE / class_weight)
- [ ] Deep Learning — TensorFlow Functional API
- [ ] Minimal 1 custom component (Layer / Loss / Callback)
- [ ] Evaluasi: Accuracy ≥ 85%, Recall ≥ 70%, ROC-AUC ≥ 0.80
- [ ] Model disimpan dalam format `.keras` atau SavedModel
- [ ] Inference code berjalan
- [ ] FastAPI endpoint `/api/v1/predict` aktif
- [ ] Preprocessing pipeline untuk 10 input field web form

**Side Quest (Nilai Tambah)**
- [ ] SHAP values di API response
- [ ] TensorBoard log tersimpan di repo
- [ ] Custom training loop dengan `tf.GradientTape`

---

---

# Jobdesk: Full-Stack Web Developer

**Anggota:** Muhammad Rifqi Indria Nugraha

## Action Item Pertama: Buat GitHub Repository

```
Nama repo : pulsevera-cc26-pru439
Visibility: Private → invite semua anggota tim
```

Setelah repo dibuat, anggota lain push ke folder masing-masing sesuai struktur di atas.

---

## Form Input: 10 Field yang Disepakati

| No | Field | Tipe | Nilai |
|---|---|---|---|
| 1 | Jenis Kelamin | Radio | Laki-laki / Perempuan |
| 2 | Kategori Usia | Dropdown | 18-24, 25-29, 30-34, ... 80+ |
| 3 | Berat Badan (kg) | Number | 30–200 |
| 4 | Tinggi Badan (cm) | Number | 100–250 |
| 5 | Aktivitas Fisik | Toggle | Ya / Tidak |
| 6 | Jam Tidur | Slider | 1–14 jam |
| 7 | Status Merokok | Dropdown | Tidak pernah / Mantan / Perokok (kadang) / Perokok (setiap hari) |
| 8 | Konsumsi Alkohol | Toggle | Ya / Tidak |
| 9 | Kondisi Kesehatan Umum | Dropdown | Buruk / Cukup / Baik / Sangat Baik / Sangat Baik Sekali |
| 10 | Riwayat Diabetes | Dropdown | Tidak / Pre-diabetes / Ya |

> BMI dihitung otomatis dari berat + tinggi — tidak perlu field BMI di form.

---

## Fase 1 — Setup & Desain (Minggu 1)

```bash
# Frontend — React + Vite + Tailwind
npm create vite@latest frontend -- --template react
cd frontend
npm install axios react-router-dom recharts
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Backend — Node.js + Express
mkdir backend && cd backend
npm init -y
npm install express cors dotenv axios helmet morgan
npm install -D nodemon
```

Buat mockup di **Figma** untuk 3 halaman: Landing, Form Input, Hasil Prediksi.

---

## Fase 2 — Frontend (Minggu 2)

```
frontend/src/
├── components/
│   ├── RiskForm/           ← Form 10 field + validasi
│   ├── ResultCard/         ← Risk score + label berwarna
│   ├── RiskFactorList/     ← Top 3 faktor + ikon + deskripsi
│   ├── RecommendationList/ ← Saran gaya hidup
│   └── RiskGauge/          ← Progress bar animasi (Recharts)
├── pages/
│   ├── Home.jsx
│   ├── CheckRisk.jsx
│   └── Result.jsx
└── services/
    └── api.js              ← Semua axios call ke backend
```

```javascript
// services/api.js
import axios from 'axios';
const API_BASE = import.meta.env.VITE_BACKEND_URL || 'http://localhost:3001';

export const predictRisk = async (formData) => {
  const response = await axios.post(`${API_BASE}/api/predict`, formData);
  return response.data;
};
```

---

## Fase 3 — Backend Express (Minggu 2–3)

Backend berfungsi sebagai **proxy** antara React dan FastAPI milik AI Engineer.

```
POST  /api/predict           ← Teruskan ke ML API, return hasil
GET   /api/health            ← Health check
POST  /api/history           ← (Side Quest) Simpan riwayat prediksi
GET   /api/history/:userId   ← (Side Quest) Ambil riwayat
```

```javascript
// routes/predict.js
router.post('/predict', async (req, res) => {
  try {
    const required = ['sex','age_category','height_meters','weight_kg',
                      'sleep_hours','physical_activities','smoker_status',
                      'alcohol','general_health'];
    const missing = required.filter(f => !req.body[f]);
    if (missing.length) return res.status(400).json({ error: `Field kosong: ${missing.join(', ')}` });

    const mlRes = await axios.post(`${process.env.ML_API_URL}/api/v1/predict`, req.body);
    res.json(mlRes.data);
  } catch (err) {
    res.status(500).json({ error: 'Gagal mendapatkan prediksi. Coba lagi.' });
  }
});
```

---

## Fase 4 — Tampilan Hasil (Minggu 4)

**Risk Score** — gauge berwarna (hijau <30%, kuning 30–60%, merah >60%)

**Top 3 Faktor Risiko** — map nama fitur dari API ke label yang user-friendly:
```javascript
const FACTOR_DESCRIPTIONS = {
  'AgeCategory':        { label: 'Usia',              icon: '👴', desc: 'Risiko meningkat signifikan seiring usia' },
  'BMI':                { label: 'Indeks Berat Badan', icon: '⚖️', desc: 'BMI tinggi meningkatkan beban jantung' },
  'SmokerStatus':       { label: 'Status Merokok',     icon: '🚬', desc: 'Merokok merusak pembuluh darah jantung' },
  'LifestyleRiskScore': { label: 'Gaya Hidup',         icon: '🏃', desc: 'Kombinasi kebiasaan tidak sehat' },
  'GeneralHealth':      { label: 'Kesehatan Umum',     icon: '🏥', desc: 'Kondisi kesehatan keseluruhan yang kurang baik' },
  'HadDiabetes':        { label: 'Diabetes',           icon: '🩺', desc: 'Diabetes meningkatkan risiko penyakit jantung' },
};
```

---

## Fase 5 — Deployment (Minggu 5)

```bash
# Frontend → Netlify / Vercel
# Set env variable: VITE_BACKEND_URL=https://your-backend.com

# Backend → Railway / Render (free tier)
# Set env variable:
# ML_API_URL=https://your-ml-api.com
# PORT=3001
```

Vercel/Netlify setting untuk subfolder:
```
Root Directory  : frontend/
Build Command   : npm run build
Output Directory: dist/
```

## Checklist Full-Stack

**Main Quest (Wajib)**
- [ ] GitHub repository dibuat, semua anggota punya akses
- [ ] Project dibangun dengan Vite (module bundler)
- [ ] Networking calls dengan Axios ke backend
- [ ] Form 10 field + validasi berjalan
- [ ] RESTful API Express — URL konvensional (`/api/predict`)
- [ ] Integrasi dengan FastAPI AI Engineer berjalan
- [ ] Tampilan hasil: risk score, top 3 faktor, rekomendasi
- [ ] Fitur utama tidak crash

**Side Quest (Nilai Tambah)**
- [ ] Mockup Figma
- [ ] Layout responsif (mobile + desktop)
- [ ] Database untuk simpan riwayat prediksi
- [ ] Deployment berhasil (Netlify/Vercel)

---

---

# Arsitektur Sistem

```
[User Browser]
      │
      ▼
┌─────────────────────┐
│   React Frontend    │  Vite · Tailwind CSS · Axios · Recharts
│   (Netlify/Vercel)  │
└──────────┬──────────┘
           │ POST /api/predict
           ▼
┌─────────────────────┐
│  Node.js/Express    │  Backend Full-Stack
│  Backend            │  (Railway / Render)
└──────────┬──────────┘
           │ POST /api/v1/predict
           ▼
┌─────────────────────┐
│  FastAPI Python     │  AI Engineer
│  Inference API      │  Scikit-learn · TensorFlow · SHAP
└──────────┬──────────┘
           │ loads
           ▼
┌─────────────────────┐
│  Trained Model      │  .keras / .pkl
│  + Preprocessing    │  Data pipeline dari DS
└─────────────────────┘
```

---

# Handoff Antar Role

## DS → AI Engineer ✅

| Deliverable | Lokasi | Status |
|---|---|---|
| X_train, X_test, y_train, y_test | `data/final/` | ✅ Siap |
| dataset_final.csv (+ 6 fitur baru) | `data/final/` | ✅ Siap |
| data_dictionary.md (47 kolom) | root | ✅ Siap |
| Encoding mapping lengkap | `notebooks/01_data_wrangling.ipynb` | ✅ Siap |
| Top correlated features + visualisasi | `notebooks/02_eda.ipynb` | ✅ Siap |

## AI Engineer → Full-Stack

| Yang Dibutuhkan | Kapan |
|---|---|
| FastAPI URL + dokumentasi endpoint | Minggu 3 |
| Format request & response JSON | Minggu 3 |
| List nama fitur output SHAP | Minggu 3 |

## Timeline Koordinasi

| Waktu | Aksi |
|---|---|
| **Sekarang** | Full-Stack buat GitHub repo, invite semua anggota |
| **Minggu 2** | AI Engineer share FastAPI lokal untuk integrasi awal |
| **Minggu 3** | Full-Stack + AI Engineer: integration test bersama |
| **Minggu 5** | Testing end-to-end seluruh sistem sebelum deployment |

---

*Dataset: CDC BRFSS 2022 | 445.132 responden | Coding Camp 2026 powered by DBS Foundation*
