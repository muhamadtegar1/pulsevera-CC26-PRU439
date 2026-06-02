"""
Pulsevera — ML Inference API
FastAPI endpoint untuk prediksi risiko penyakit jantung.

Hybrid implementation:
- Struktur modular (preprocessing.py, inference.py, train.py) dari Shafira
- Integrasi Gemini AI untuk recommendations dari Fathan
- Fallback rule-based bila Gemini tidak tersedia

Run lokal:
    cd ml-api
    uvicorn main:app --reload --port 8000

Endpoints:
    GET  /                  — Info API
    GET  /health            — Liveness + status model + status Gemini
    GET  /api/v1/metadata   — Metadata model + fitur penting (SHAP global)
    POST /api/v1/predict    — Prediksi risiko (ML)
    POST /api/v1/predict-dl — Prediksi risiko (Deep Learning) bila tersedia
"""
from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

import inference
import preprocessing

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
log = logging.getLogger('pulsevera-api')

app = FastAPI(
    title='Pulsevera ML API',
    description='API prediksi risiko penyakit jantung — Coding Camp 2026 CC26-PRU439.',
    version='1.0.0',
    contact={'name': 'Pulsevera AI Engineer (Fathan & Shafira)'},
)

_ALLOWED_ORIGINS = os.getenv(
    'ALLOWED_ORIGINS',
    'http://localhost:5173,http://localhost:3001'
).split(',')
# Lokal dev: localhost diizinkan. Production: set env ALLOWED_ORIGINS dengan domain Vercel/Netlify.
if '*' in _ALLOWED_ORIGINS or os.getenv('ALLOWED_ORIGINS') is None:
    _ALLOWED_ORIGINS = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=_ALLOWED_ORIGINS,
    allow_methods=['*'],
    allow_headers=['*'],
)


# ── Gemini config ─────────────────────────────────────────────────────
GEMINI_API_KEY_PLACEHOLDER = "PASTE_YOUR_GEMINI_API_KEY_HERE"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", GEMINI_API_KEY_PLACEHOLDER)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_FALLBACK_MODELS = os.getenv("GEMINI_FALLBACK_MODELS", "gemini-2.0-flash")
GEMINI_ENABLED = os.getenv("GEMINI_ENABLED", "true").lower() == "true"

gemini_client = None

AGE_CATEGORY_LABELS = {
    1: "18-24", 2: "25-29", 3: "30-34", 4: "35-39", 5: "40-44",
    6: "45-49", 7: "50-54", 8: "55-59", 9: "60-64", 10: "65-69",
    11: "70-74", 12: "75-79", 13: "80+",
}

GEMINI_RECOMMENDATION_PROMPT = """
Anda adalah asisten rekomendasi gaya hidup untuk Pulsevera, aplikasi edukasi
risiko penyakit jantung. Buat rekomendasi yang personal berdasarkan profil
pengguna dan faktor risiko prioritas yang diberikan.

Aturan wajib:
- Jawab dalam Bahasa Indonesia.
- Output hanya JSON object valid dengan key "recommendations".
- Isi "recommendations" harus berupa tepat 3 string.
- Setiap rekomendasi maksimal 22 kata, konkret, aman, dan dapat dilakukan.
- Jangan menyebut skor, probabilitas, model, machine learning, atau deep learning.
- Jangan mendiagnosis penyakit dan jangan memberi dosis obat atau suplemen.
- Jika ada faktor diabetes, perokok aktif, obesitas, usia 60+, atau kesehatan umum buruk, anjurkan konsultasi tenaga kesehatan.
- Hindari kalimat menakut-nakuti; gunakan nada profesional dan suportif.
- Tone WAJIB konsisten dengan label_risiko dalam profil:
  * label_risiko "Rendah": nada positif, fokus pemeliharaan — JANGAN anjurkan konsultasi darurat atau tindakan segera.
  * label_risiko "Sedang": nada suportif dan proaktif, dorong evaluasi rutin.
  * label_risiko "Tinggi": nada tegas tapi empati, anjurkan konsultasi tenaga kesehatan dalam waktu dekat.
"""


class GeminiRecommendationResponse(BaseModel):
    recommendations: list[str]


def get_gemini_inactive_reason() -> Optional[str]:
    if not GEMINI_ENABLED:
        return "GEMINI_ENABLED=false"
    if genai is None or types is None:
        return "package google-genai belum terpasang di environment Python ini"
    api_key = (GEMINI_API_KEY or "").strip()
    if not api_key or api_key == GEMINI_API_KEY_PLACEHOLDER:
        return "GEMINI_API_KEY belum diisi atau masih placeholder"
    return None


def create_gemini_client():
    if get_gemini_inactive_reason() is not None:
        return None
    api_key = (GEMINI_API_KEY or "").strip()
    return genai.Client(api_key=api_key)


def get_gemini_model_candidates() -> list[str]:
    model_names = [GEMINI_MODEL]
    model_names.extend(
        m.strip() for m in GEMINI_FALLBACK_MODELS.split(",") if m.strip()
    )
    deduped = []
    for m in model_names:
        if m not in deduped:
            deduped.append(m)
    return deduped


_TONE_GUIDE = {
    "Rendah": "Nada: positif dan motivasi. Fokus pemeliharaan — jangan anjurkan konsultasi darurat.",
    "Sedang": "Nada: suportif dan proaktif. Dorong evaluasi rutin dengan dokter.",
    "Tinggi": "Nada: tegas tapi empati. Anjurkan konsultasi tenaga kesehatan dalam waktu dekat.",
}

_LIFESTYLE_NOTE = {
    "Sangat Sehat": "Gaya hidup sudah sangat baik — fokus pada konsistensi dan pemeliharaan.",
    "Sehat": "Gaya hidup baik — ada satu aspek kecil yang bisa ditingkatkan.",
    "Cukup": "Beberapa kebiasaan perlu diperbaiki — mulai dari yang paling mudah.",
    "Perlu Perhatian": "Beberapa kebiasaan berisiko — prioritaskan perubahan yang paling berdampak.",
    "Berisiko": "Banyak kebiasaan berisiko — butuh perubahan bertahap yang konsisten.",
    "Berisiko Tinggi": "Gaya hidup berisiko tinggi — mulai perubahan sekarang dan konsultasi dokter.",
}


def build_gemini_prompt(
    user_input: dict[str, Any],
    top_factors_labels: list[str],
    risk_label: str = "Rendah",
    lifestyle_grade: str = "Cukup",
) -> str:
    bmi = float(user_input["weight_kg"]) / (float(user_input["height_meters"]) ** 2)
    age_category = int(user_input.get("age_category", 1))
    profile = {
        "jenis_kelamin": user_input.get("sex"),
        "rentang_usia": AGE_CATEGORY_LABELS.get(age_category, f"Kategori {age_category}"),
        "bmi": round(bmi, 1),
        "jam_tidur": user_input.get("sleep_hours"),
        "aktivitas_fisik": user_input.get("physical_activities"),
        "status_merokok": user_input.get("smoker_status"),
        "alkohol": user_input.get("alcohol"),
        "kesehatan_umum": user_input.get("general_health"),
        "diabetes": user_input.get("diabetes", "No"),
        "label_risiko": risk_label,
        "grade_gaya_hidup": lifestyle_grade,
    }
    tone = _TONE_GUIDE.get(risk_label, "Nada: profesional dan suportif.")
    lifestyle_note = _LIFESTYLE_NOTE.get(lifestyle_grade, "")
    return (
        "Buat 3 rekomendasi gaya hidup untuk profil berikut.\n"
        f"Profil pengguna:\n{json.dumps(profile, ensure_ascii=False, indent=2)}\n"
        f"Faktor risiko prioritas:\n{json.dumps(top_factors_labels, ensure_ascii=False)}\n"
        f"{tone}\n"
        f"{lifestyle_note}\n"
        "Fokus pada perubahan perilaku yang paling relevan untuk faktor risiko tersebut."
    )


def build_gemini_config(model_name: str):
    config = {
        "system_instruction": GEMINI_RECOMMENDATION_PROMPT,
        "temperature": 0.4,
        "max_output_tokens": 1024,
        "response_mime_type": "application/json",
        "response_schema": GeminiRecommendationResponse,
    }
    if "2.5" in model_name:
        config["thinking_config"] = types.ThinkingConfig(thinking_budget=0)
    return types.GenerateContentConfig(**config)


def normalize_recommendations(recommendations: Any) -> list[str]:
    if not isinstance(recommendations, list):
        return []
    clean = []
    for item in recommendations:
        if isinstance(item, str) and item.strip():
            clean.append(item.strip())
    return clean[:3]


def parse_gemini_response(response: Any) -> list[str]:
    parsed = getattr(response, "parsed", None)
    if isinstance(parsed, GeminiRecommendationResponse):
        return normalize_recommendations(parsed.recommendations)
    if isinstance(parsed, dict):
        return normalize_recommendations(parsed.get("recommendations"))
    raw_text = (getattr(response, "text", None) or "").strip()
    if not raw_text:
        return []
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError:
        return []
    recs = payload.get("recommendations") if isinstance(payload, dict) else payload
    return normalize_recommendations(recs)


def get_gemini_recommendations(
    user_input: dict[str, Any],
    top_factors: list[str],
    risk_label: str = "Rendah",
    lifestyle_grade: str = "Cukup",
) -> list[str]:
    if gemini_client is None or types is None:
        return []
    factor_labels = [inference.factor_to_label(f) for f in top_factors]
    for model_name in get_gemini_model_candidates():
        try:
            response = gemini_client.models.generate_content(
                model=model_name,
                contents=build_gemini_prompt(user_input, factor_labels, risk_label, lifestyle_grade),
                config=build_gemini_config(model_name),
            )
            recs = parse_gemini_response(response)
            if recs:
                if model_name != GEMINI_MODEL:
                    log.info("Gemini fallback model: %s", model_name)
                return recs
            log.warning("Gemini model %s returned empty recommendations.", model_name)
        except Exception as exc:
            log.warning("Gemini model %s failed: %s", model_name, exc)
    log.warning("All Gemini models failed — using rule-based fallback.")
    return []


# ── Schemas ───────────────────────────────────────────────────────────
class UserInput(BaseModel):
    sex: str = Field(..., example='Male')
    age_category: int = Field(..., ge=1, le=13, example=7)
    height_meters: float = Field(..., ge=1.0, le=2.5, example=1.70)
    weight_kg: float = Field(..., ge=30, le=200, example=70.0)
    sleep_hours: float = Field(..., ge=1, le=14, example=7.0)
    physical_activities: str = Field(..., example='Yes')
    smoker_status: str = Field(..., example='Never')
    alcohol: str = Field(..., example='No')
    general_health: str = Field(..., example='Good')
    diabetes: Optional[str] = Field(default='No', example='No')


class RiskFactor(BaseModel):
    feature: str
    label: str


class LifestyleHabit(BaseModel):
    key: str
    label: str
    good: bool


class LifestyleScore(BaseModel):
    score: int = Field(..., description='Skor gaya hidup 0–5 (5 = paling sehat)')
    max_score: int = 5
    grade: str = Field(..., description='"Sangat Sehat" | "Sehat" | "Cukup" | "Perlu Perhatian" | "Berisiko"')
    habits: list[LifestyleHabit] = Field(..., description='Breakdown 5 kebiasaan: smoking, exercise, sleep, weight, alcohol')


class PredictionResult(BaseModel):
    risk_score: float = Field(..., description='Probabilitas 0.0–1.0 untuk HadHeartAttack=Yes')
    risk_percent: float = Field(..., description='risk_score x 100')
    risk_label: str = Field(..., description='"Rendah" | "Sedang" | "Tinggi"')
    lifestyle: LifestyleScore = Field(..., description='Skor gaya hidup primary metric, complementary ke risk_score')
    top_risk_factors: list[RiskFactor]
    recommendations: list[str]
    recommendation_source: str = Field(..., description='"gemini" | "rule_based"')
    model_used: str
    inference_ms: float


class MetadataResponse(BaseModel):
    model_loaded: bool
    dl_model_loaded: bool
    best_model_name: Optional[str] = None
    n_features: Optional[int] = None
    needs_scaling: Optional[bool] = None
    trained_at: Optional[str] = None
    ml_metrics: dict = {}
    dl_metrics: dict = {}
    shap_top_factors: dict = {}


# ── Startup ───────────────────────────────────────────────────────────
@app.on_event('startup')
def on_startup() -> None:
    global gemini_client
    log.info('Loading Pulsevera models...')
    try:
        inference.bundle.load()
        if not inference.bundle.ready:
            log.warning(
                'Model belum dilatih — jalankan `python train.py` di folder ml-api/.'
            )
    except Exception as exc:
        log.exception('Gagal memuat model: %s', exc)

    gemini_client = create_gemini_client()
    if gemini_client is None:
        reason = get_gemini_inactive_reason() or "client Gemini tidak tersedia"
        log.info("Gemini belum aktif (%s) — rekomendasi memakai fallback rule-based.", reason)
    else:
        log.info("Gemini aktif untuk rekomendasi. Model: %s", GEMINI_MODEL)


# ── Endpoints ─────────────────────────────────────────────────────────
@app.get('/')
async def root():
    return {
        'service': 'Pulsevera ML API',
        'version': '1.0.0',
        'docs': '/docs',
        'health': '/health',
        'predict': '/api/v1/predict',
    }


@app.get('/health')
async def health_check():
    b = inference.bundle
    gemini_active = gemini_client is not None
    return {
        'status': 'ok',
        'model_loaded': b.ml_model is not None,
        'dl_model_loaded': b.dl_model is not None,
        'scaler_loaded': b.scaler is not None,
        'gemini_recommendations': gemini_active,
        'gemini_model': GEMINI_MODEL,
        'gemini_model_candidates': get_gemini_model_candidates(),
        'gemini_inactive_reason': None if gemini_active else get_gemini_inactive_reason(),
    }


@app.get('/api/v1/metadata', response_model=MetadataResponse)
async def metadata():
    b = inference.bundle
    shap_path = BASE_DIR / 'models' / 'shap_metadata.json'
    shap_top: dict = {}
    if shap_path.exists():
        with open(shap_path) as f:
            shap_top = json.load(f).get('global_importance_top10', {})

    ml_results: dict = {}
    ml_results_path = BASE_DIR / 'models' / 'ml_results.json'
    if ml_results_path.exists():
        with open(ml_results_path) as f:
            ml_results = json.load(f)

    return MetadataResponse(
        model_loaded=b.ml_model is not None,
        dl_model_loaded=b.dl_model is not None,
        best_model_name=b.feature_meta.get('best_model_name'),
        n_features=b.feature_meta.get('n_features'),
        needs_scaling=b.feature_meta.get('needs_scaling'),
        trained_at=b.feature_meta.get('trained_at'),
        ml_metrics=ml_results,
        dl_metrics=b.dl_meta,
        shap_top_factors=shap_top,
    )


def _resolve_recommendations(
    user_input: dict,
    top_features: list[str],
    risk_label: str = "Rendah",
    lifestyle_grade: str = "Cukup",
) -> tuple[list[str], str]:
    """Coba Gemini dulu, fallback ke rule-based bila gagal."""
    gemini_recs = get_gemini_recommendations(user_input, top_features, risk_label, lifestyle_grade)
    if gemini_recs:
        return gemini_recs, "gemini"
    rule_based = inference.generate_recommendations(user_input, top_features)
    return rule_based, "rule_based"


def compute_lifestyle_score(user_input: dict[str, Any]) -> LifestyleScore:
    """Skor gaya hidup 0–5 dihitung dari 5 kebiasaan keseharian.

    Sejajar dengan feature engineering DS (LifestyleRiskScore), tapi
    di-INVERSI agar score TINGGI = LEBIH BAIK (lebih intuitif untuk end user).

    Skor 5 = 5 kebiasaan baik semua
    Skor 0 = 5 kebiasaan buruk semua
    """
    sex = user_input.get('sex', 'Male')
    smoker = user_input.get('smoker_status', 'Never')
    exercise = user_input.get('physical_activities', 'Yes')
    sleep = float(user_input.get('sleep_hours', 7))
    alcohol = user_input.get('alcohol', 'No')

    height = float(user_input.get('height_meters', 1.7))
    weight = float(user_input.get('weight_kg', 70))
    bmi = weight / (height ** 2)

    # 5 habit indicators (True = good habit)
    not_smoking = smoker in ('Never', 'Former')
    active = exercise == 'Yes'
    enough_sleep = 6 <= sleep <= 9
    healthy_weight = 18.5 <= bmi < 30
    not_drinking = alcohol == 'No'

    score = sum([not_smoking, active, enough_sleep, healthy_weight, not_drinking])

    grade_map = {
        5: 'Sangat Sehat',
        4: 'Sehat',
        3: 'Cukup',
        2: 'Perlu Perhatian',
        1: 'Berisiko',
        0: 'Berisiko Tinggi',
    }
    grade = grade_map[score]

    habits = [
        LifestyleHabit(
            key='not_smoking',
            label='Tidak merokok aktif' if not_smoking else 'Masih merokok aktif',
            good=not_smoking,
        ),
        LifestyleHabit(
            key='active',
            label='Aktif berolahraga' if active else 'Kurang aktivitas fisik',
            good=active,
        ),
        LifestyleHabit(
            key='enough_sleep',
            label=f'Pola tidur sehat ({sleep:.0f} jam)' if enough_sleep else f'Pola tidur kurang ideal ({sleep:.0f} jam)',
            good=enough_sleep,
        ),
        LifestyleHabit(
            key='healthy_weight',
            label=f'BMI ideal ({bmi:.1f})' if healthy_weight else f'BMI di luar normal ({bmi:.1f})',
            good=healthy_weight,
        ),
        LifestyleHabit(
            key='not_drinking',
            label='Tidak konsumsi alkohol' if not_drinking else 'Konsumsi alkohol',
            good=not_drinking,
        ),
    ]

    return LifestyleScore(score=score, max_score=5, grade=grade, habits=habits)


def _predict_core(user_input: UserInput, prefer: str) -> PredictionResult:
    # Fallback: bila ML model tidak tersedia (mis. deployment tanpa pkl besar),
    # otomatis gunakan DL model. Berguna di Hugging Face Spaces / cloud deployment.
    if prefer == 'ml' and inference.bundle.ml_model is None:
        if inference.bundle.dl_model is not None:
            prefer = 'dl'
        else:
            raise HTTPException(
                status_code=503,
                detail='Model ML belum dilatih. Jalankan `python train.py` di folder ml-api/.',
            )
    if prefer == 'dl' and inference.bundle.dl_model is None:
        raise HTTPException(
            status_code=503,
            detail='Model DL belum tersedia. Jalankan `python train.py` (tanpa --skip-dl).',
        )

    t0 = time.perf_counter()
    payload = user_input.model_dump()
    try:
        input_df = preprocessing.preprocess_user_input(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    proba = inference.predict_proba(input_df, prefer=prefer)
    top_features = inference.get_top_risk_factors(input_df, top_n=3)
    label = inference.risk_label(proba)
    lifestyle = compute_lifestyle_score(payload)
    recommendations, rec_source = _resolve_recommendations(
        payload, top_features, risk_label=label, lifestyle_grade=lifestyle.grade
    )

    elapsed_ms = (time.perf_counter() - t0) * 1000
    model_used = (
        inference.bundle.dl_meta.get('architecture', 'Deep Learning')
        if prefer == 'dl'
        else inference.bundle.feature_meta.get('best_model_name', 'ML Model')
    )

    return PredictionResult(
        risk_score=round(proba, 4),
        risk_percent=round(proba * 100, 2),
        risk_label=label,
        lifestyle=lifestyle,
        top_risk_factors=[
            RiskFactor(feature=f, label=inference.factor_to_label(f)) for f in top_features
        ],
        recommendations=recommendations,
        recommendation_source=rec_source,
        model_used=model_used,
        inference_ms=round(elapsed_ms, 2),
    )


@app.post('/api/v1/predict', response_model=PredictionResult)
async def predict(user_input: UserInput):
    """Prediksi via Deep Learning model (default, sesuai keputusan tim AI Engineer).

    DL + SMOTE @ threshold 0.23: Acc 85.76%, Recall 71.15%, ROC-AUC 0.881.
    """
    return _predict_core(user_input, prefer='dl')


@app.post('/api/v1/predict-ml', response_model=PredictionResult)
async def predict_ml(user_input: UserInput):
    """Prediksi via Random Forest baseline (alternatif untuk benchmarking)."""
    return _predict_core(user_input, prefer='ml')
