"""
Pulsevera — Inference Engine
Memuat model ML (.pkl) atau DL (.keras), generate prediksi,
ekstraksi top risk factors via SHAP, dan rekomendasi gaya hidup.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

import joblib
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / 'models'


# ── Mapping label fitur model -> teks user-friendly Indonesia ────────
FACTOR_LABEL_ID: dict[str, str] = {
    'AgeCategory': 'Usia',
    'BMI': 'Indeks Massa Tubuh (BMI)',
    'WeightInKilograms': 'Berat Badan',
    'HeightInMeters': 'Tinggi Badan',
    'SmokerStatus': 'Status Merokok',
    'IsActiveSmoker': 'Perokok Aktif',
    'AlcoholDrinkers': 'Konsumsi Alkohol',
    'SleepHours': 'Jam Tidur',
    'IsSleepDeprived': 'Kurang Tidur',
    'PhysicalActivities': 'Aktivitas Fisik',
    'GeneralHealth': 'Kondisi Kesehatan Umum',
    'HadDiabetes': 'Riwayat Diabetes',
    'HadAngina': 'Riwayat Angina',
    'HadStroke': 'Riwayat Stroke',
    'HadAsthma': 'Riwayat Asma',
    'HadCOPD': 'Penyakit Paru Kronis',
    'HadKidneyDisease': 'Penyakit Ginjal',
    'HadArthritis': 'Riwayat Artritis',
    'HadDepressiveDisorder': 'Gangguan Depresi',
    'LifestyleRiskScore': 'Skor Gaya Hidup',
    'HasChronicCondition': 'Kondisi Kronis',
    'PoorHealthDays_Total': 'Hari Tidak Sehat',
    'PhysicalHealthDays': 'Hari Fisik Buruk',
    'MentalHealthDays': 'Hari Mental Buruk',
    'Sex': 'Jenis Kelamin',
    'IsObese': 'Obesitas',
    'ChestScan': 'Riwayat CT Scan Dada',
}


# ── Model holder singleton ────────────────────────────────────────────
class ModelBundle:
    """Cache model + metadata supaya tidak di-load berulang per request."""

    def __init__(self) -> None:
        self.ml_model = None
        self.dl_model = None
        self.scaler = None
        self.explainer = None
        self.feature_meta: dict = {}
        self.dl_meta: dict = {}
        self.feature_order: list[str] = []

    @property
    def ready(self) -> bool:
        return self.ml_model is not None or self.dl_model is not None

    def load(self) -> None:
        meta_path = MODELS_DIR / 'feature_metadata.json'
        if meta_path.exists():
            with open(meta_path) as f:
                self.feature_meta = json.load(f)
            self.feature_order = self.feature_meta.get('feature_order', [])

        dl_meta_path = MODELS_DIR / 'dl_metadata.json'
        if dl_meta_path.exists():
            with open(dl_meta_path) as f:
                self.dl_meta = json.load(f)

        # ML model (joblib pickle)
        ml_path = MODELS_DIR / 'pulsevera_ml_model.pkl'
        if ml_path.exists():
            self.ml_model = joblib.load(ml_path)
            logger.info('ML model loaded: %s', ml_path.name)

        # Scaler
        scaler_path = MODELS_DIR / 'scaler.pkl'
        if scaler_path.exists():
            self.scaler = joblib.load(scaler_path)
            logger.info('Scaler loaded')

        # DL model (Keras)
        dl_path = MODELS_DIR / 'pulsevera_dl_model.keras'
        if dl_path.exists():
            try:
                import tensorflow as tf
                import keras

                @keras.saving.register_keras_serializable(
                    package='pulsevera', name='focal_loss'
                )
                def focal_loss(y_true, y_pred, gamma=2.0, alpha=0.25):
                    y_true = tf.cast(y_true, tf.float32)
                    y_pred = tf.clip_by_value(y_pred, 1e-7, 1 - 1e-7)
                    bce = -(y_true * tf.math.log(y_pred)
                            + (1 - y_true) * tf.math.log(1 - y_pred))
                    p_t = y_true * y_pred + (1 - y_true) * (1 - y_pred)
                    alpha_t = y_true * alpha + (1 - y_true) * (1 - alpha)
                    return tf.reduce_mean(alpha_t * tf.pow(1.0 - p_t, gamma) * bce)

                self.dl_model = keras.models.load_model(
                    dl_path,
                    custom_objects={'focal_loss': focal_loss},
                    safe_mode=False,
                )
                logger.info('DL model loaded: %s', dl_path.name)
            except Exception as exc:
                logger.warning('Gagal load DL model: %s', exc)

        # SHAP explainer (optional, lazy)
        explainer_path = MODELS_DIR / 'shap_explainer.pkl'
        if explainer_path.exists():
            try:
                self.explainer = joblib.load(explainer_path)
                logger.info('SHAP explainer loaded')
            except Exception as exc:
                logger.warning('Gagal load SHAP explainer: %s', exc)


bundle = ModelBundle()


# ── Prediksi ──────────────────────────────────────────────────────────
def predict_proba(input_df: pd.DataFrame, prefer: str = 'ml') -> float:
    """Return probabilitas kelas positif (HadHeartAttack=1)."""
    if prefer == 'dl' and bundle.dl_model is not None:
        X = input_df.values.astype('float32')
        if bundle.scaler is not None:
            X = bundle.scaler.transform(X).astype('float32')
        proba = float(bundle.dl_model.predict(X, verbose=0).ravel()[0])
        return proba

    if bundle.ml_model is None:
        raise RuntimeError('ML model belum dimuat. Jalankan train.py terlebih dahulu.')

    X = input_df.values
    if bundle.feature_meta.get('needs_scaling') and bundle.scaler is not None:
        X = bundle.scaler.transform(X)
    return float(bundle.ml_model.predict_proba(X)[0][1])


def risk_label(prob: float) -> str:
    """Konversi probability ke risk label.

    Boundary align dengan operational threshold DL model = 0.23 (sweet spot
    yang disepakati tim: Acc >= 85%, Recall >= 70% pada threshold 0.23).
    - < 0.23      => Rendah (model klasifikasi negatif)
    - 0.23 - 0.40 => Sedang (di atas threshold positif, tapi belum tinggi)
    - >= 0.40     => Tinggi (probability tinggi terhadap kelas positif)
    """
    if prob < 0.23:
        return 'Rendah'
    if prob < 0.40:
        return 'Sedang'
    return 'Tinggi'


# ── SHAP top risk factors ─────────────────────────────────────────────
def _ensure_explainer():
    """Bangun TreeExplainer / LinearExplainer / KernelExplainer on demand."""
    if bundle.explainer is not None:
        return bundle.explainer
    if bundle.ml_model is None:
        return None

    try:
        import shap
    except ImportError:
        logger.warning('SHAP belum terpasang — fallback ke feature_importances_')
        return None

    if hasattr(bundle.ml_model, 'estimators_'):
        bundle.explainer = shap.TreeExplainer(bundle.ml_model)
    elif hasattr(bundle.ml_model, 'coef_'):
        means = bundle.feature_meta.get('feature_means', {})
        if bundle.feature_order and means:
            bg = pd.DataFrame([means])[bundle.feature_order].values
            if bundle.scaler is not None:
                bg = bundle.scaler.transform(bg)
            bundle.explainer = shap.LinearExplainer(
                bundle.ml_model, bg, feature_names=bundle.feature_order,
            )
    return bundle.explainer


def get_top_risk_factors(
    input_df: pd.DataFrame,
    top_n: int = 3,
    feature_names: Optional[list[str]] = None,
) -> list[str]:
    """Return top-N nama fitur dengan kontribusi |SHAP| tertinggi."""
    feature_names = feature_names or bundle.feature_order or input_df.columns.tolist()

    explainer = _ensure_explainer()
    if explainer is not None:
        try:
            X = input_df.values
            if bundle.feature_meta.get('needs_scaling') and bundle.scaler is not None:
                X = bundle.scaler.transform(X)
            sv = explainer.shap_values(X)
            if isinstance(sv, list):
                sv = sv[1] if len(sv) > 1 else sv[0]
            arr = np.asarray(sv)
            if arr.ndim == 3:
                arr = arr[:, :, 1]
            contributions = pd.Series(arr[0], index=feature_names)
            return contributions.abs().nlargest(top_n).index.tolist()
        except Exception as exc:
            logger.warning('SHAP gagal (%s); fallback ke feature_importances_', exc)

    # Fallback: feature_importances_ atau koefisien linear
    if hasattr(bundle.ml_model, 'feature_importances_'):
        imp = pd.Series(bundle.ml_model.feature_importances_, index=feature_names)
        return imp.nlargest(top_n).index.tolist()
    if hasattr(bundle.ml_model, 'coef_'):
        imp = pd.Series(np.abs(bundle.ml_model.coef_[0]), index=feature_names)
        return imp.nlargest(top_n).index.tolist()
    return feature_names[:top_n]


# ── Rekomendasi gaya hidup ────────────────────────────────────────────
def _factor_recommendation(factor: str, user_input: dict) -> Optional[str]:
    """Rekomendasi spesifik per faktor risiko, sesuai input user."""
    if factor in ('SmokerStatus', 'IsActiveSmoker'):
        if user_input.get('smoker_status', 'Never') not in ('Never',):
            return 'Berhenti merokok — risiko serangan jantung turun signifikan dalam 1 tahun setelah berhenti.'

    if factor in ('BMI', 'IsObese', 'WeightInKilograms'):
        h = float(user_input.get('height_meters', 1.7))
        w = float(user_input.get('weight_kg', 70))
        bmi = w / (h ** 2)
        if bmi >= 30:
            return 'BMI tergolong obesitas. Targetkan penurunan berat 5–10% melalui pola makan seimbang dan olahraga rutin.'
        if bmi >= 25:
            return 'BMI di atas normal. Pertahankan diet seimbang dan aktif bergerak minimal 150 menit/minggu.'

    if factor == 'PhysicalActivities' and user_input.get('physical_activities', 'Yes') == 'No':
        return 'Mulai aktivitas fisik 30 menit/hari (jalan cepat, bersepeda, berenang) minimal 5 hari/minggu.'

    if factor in ('SleepHours', 'IsSleepDeprived'):
        sh = float(user_input.get('sleep_hours', 7))
        if sh < 6:
            return f'Jam tidur ({sh} jam) di bawah rekomendasi. Targetkan 7–9 jam/hari dan jaga konsistensi waktu tidur.'
        if sh > 9:
            return 'Jam tidur berlebihan juga berisiko. Konsultasikan ke dokter bila mengantuk berlebihan di siang hari.'

    if factor == 'AlcoholDrinkers' and user_input.get('alcohol') == 'Yes':
        return 'Batasi konsumsi alkohol — tidak lebih dari 1 gelas/hari (perempuan) atau 2 gelas/hari (laki-laki).'

    if factor == 'HadDiabetes' and user_input.get('diabetes', 'No') != 'No':
        return 'Kelola diabetes dengan kontrol gula darah rutin, diet rendah karbohidrat sederhana, dan obat sesuai anjuran dokter.'

    if factor == 'GeneralHealth':
        if user_input.get('general_health') in ('Poor', 'Fair'):
            return 'Lakukan medical check-up lengkap untuk mengidentifikasi penyebab kondisi kesehatan yang kurang baik.'

    if factor == 'AgeCategory':
        age = int(user_input.get('age_category', 1))
        if age >= 9:
            return 'Usia adalah faktor risiko yang tidak bisa diubah — kompensasi dengan check-up jantung tahunan dan gaya hidup sehat.'

    if factor == 'LifestyleRiskScore':
        return 'Skor gaya hidup berisiko. Mulai dari satu kebiasaan kecil (mis. jalan kaki 20 menit/hari) lalu tambah perlahan.'

    if factor == 'HasChronicCondition':
        return 'Kondisi kronis ada — pastikan pengobatan rutin dan kontrol berkala ke dokter spesialis.'

    if factor in ('HadAngina', 'HadStroke', 'HadCOPD', 'HadKidneyDisease'):
        return 'Riwayat penyakit ini memerlukan pengawasan medis ketat dan obat-obatan rutin sesuai resep dokter.'

    return None


GENERIC_RECS = [
    'Konsumsi makanan tinggi serat (sayur, buah, biji-bijian utuh) dan kurangi makanan ultra-proses.',
    'Periksa tekanan darah, kolesterol, dan gula darah minimal 1x/tahun.',
    'Kelola stres dengan teknik relaksasi (meditasi, pernapasan dalam, hobi).',
    'Batasi asupan garam <5g/hari untuk menjaga tekanan darah.',
]


def generate_recommendations(
    user_input: dict, risk_factors: list[str], max_items: int = 5,
) -> list[str]:
    """Generate rekomendasi gaya hidup, kombinasi spesifik + generik."""
    recs: list[str] = []
    seen: set[str] = set()
    for f in risk_factors:
        rec = _factor_recommendation(f, user_input)
        if rec and rec not in seen:
            recs.append(rec)
            seen.add(rec)
        if len(recs) >= max_items:
            return recs

    for rec in GENERIC_RECS:
        if rec not in seen:
            recs.append(rec)
            seen.add(rec)
        if len(recs) >= max_items:
            break
    return recs


def factor_to_label(factor: str) -> str:
    """Label user-friendly Bahasa Indonesia untuk nama fitur model."""
    return FACTOR_LABEL_ID.get(factor, factor)
