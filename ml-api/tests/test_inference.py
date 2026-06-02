"""Unit test inference.py — logika non-model: risk_label, _is_value_risky,
get_top_risk_factors, generate_recommendations, factor_to_label."""
from __future__ import annotations

import pandas as pd
import pytest

import inference
from preprocessing import preprocess_user_input


# ── risk_label: boundary threshold 0.23 / 0.40 ────────────────────────
@pytest.mark.parametrize("prob,expected", [
    (0.0, "Rendah"),
    (0.2299, "Rendah"),
    (0.23, "Sedang"),    # tepat di threshold operasional
    (0.39, "Sedang"),
    (0.40, "Tinggi"),
    (0.99, "Tinggi"),
])
def test_risk_label_boundaries(prob, expected):
    assert inference.risk_label(prob) == expected


# ── _is_value_risky: threshold domain knowledge ───────────────────────
@pytest.mark.parametrize("feature,value,risky", [
    ("AgeCategory", 9, True),    # 60+
    ("AgeCategory", 8, False),
    ("BMI", 30, True),           # obesitas
    ("BMI", 18.0, True),         # underweight
    ("BMI", 22, False),
    ("SmokerStatus", 2, True),   # current smoker
    ("SmokerStatus", 1, False),  # former -> tidak risky
    ("SleepHours", 5, True),
    ("SleepHours", 7, False),
    ("PhysicalActivities", 0, True),  # tidak olahraga
    ("PhysicalActivities", 1, False),
    ("GeneralHealth", 2, True),  # Fair
    ("GeneralHealth", 3, False), # Good
    ("HadDiabetes", 1, True),
    ("HadDiabetes", 0, False),
])
def test_is_value_risky(feature, value, risky):
    assert inference._is_value_risky(feature, value) is risky


def test_is_value_risky_unknown_feature():
    assert inference._is_value_risky("UnknownFeature", 999) is False


def test_is_value_risky_bad_value():
    assert inference._is_value_risky("BMI", "not-a-number") is False


# ── get_top_risk_factors ──────────────────────────────────────────────
def test_top_factors_prioritizes_risky(loaded_bundle):
    """User obesitas+perokok+tua: fitur risky harus muncul."""
    df = preprocess_user_input({
        "sex": "Male", "age_category": 11, "height_meters": 1.70, "weight_kg": 100.0,
        "sleep_hours": 5.0, "physical_activities": "No", "smoker_status": "Current-every",
        "alcohol": "Yes", "general_health": "Poor", "diabetes": "Yes"})
    top = inference.get_top_risk_factors(df, top_n=3)
    assert len(top) == 3
    # minimal satu fitur yang memang risky untuk user ini
    assert any(inference._is_value_risky(f, df.iloc[0][f]) for f in top)


def test_top_factors_healthy_user_still_returns(loaded_bundle, valid_payload):
    """User sehat: tetap balik top_n (jalur fallback), tidak kosong."""
    df = preprocess_user_input(valid_payload)
    top = inference.get_top_risk_factors(df, top_n=3)
    assert len(top) == 3
    assert all(isinstance(f, str) for f in top)


def test_top_factors_no_model_returns_first_n(monkeypatch, tmp_path):
    """Tanpa model & tanpa metadata -> kembalikan N fitur pertama."""
    monkeypatch.setattr(inference, "MODELS_DIR", tmp_path)  # dir kosong, no shap_metadata
    b = inference.bundle
    saved = (b.ml_model, b.feature_order)
    b.ml_model = None
    b.feature_order = ["A", "B", "C", "D"]
    try:
        df = pd.DataFrame([{"A": 1, "B": 2, "C": 3, "D": 4}])
        top = inference.get_top_risk_factors(df, top_n=2, feature_names=["A", "B", "C", "D"])
        assert top == ["A", "B"]
    finally:
        b.ml_model, b.feature_order = saved


# ── generate_recommendations ──────────────────────────────────────────
def test_recommendations_smoker_gets_quit_advice():
    user = {"smoker_status": "Current-every"}
    recs = inference.generate_recommendations(user, ["SmokerStatus"])
    assert any("merokok" in r.lower() for r in recs)


def test_recommendations_obese_message():
    user = {"height_meters": 1.70, "weight_kg": 100.0}  # BMI ~34.6
    recs = inference.generate_recommendations(user, ["BMI"])
    assert any("obesitas" in r.lower() for r in recs)


def test_recommendations_deduped():
    user = {"smoker_status": "Current-every"}
    recs = inference.generate_recommendations(user, ["SmokerStatus", "IsActiveSmoker"])
    assert len(recs) == len(set(recs))


def test_recommendations_respects_max_items():
    user = {"smoker_status": "Current-every", "height_meters": 1.7, "weight_kg": 100,
            "physical_activities": "No", "sleep_hours": 4, "alcohol": "Yes"}
    factors = ["SmokerStatus", "BMI", "PhysicalActivities", "SleepHours", "AlcoholDrinkers"]
    recs = inference.generate_recommendations(user, factors, max_items=3)
    assert len(recs) == 3


def test_recommendations_always_filled_for_healthy_user(valid_payload):
    """User sehat tanpa faktor spesifik -> tetap dapat saran generik."""
    recs = inference.generate_recommendations(valid_payload, [])
    assert len(recs) > 0


# ── factor_to_label ───────────────────────────────────────────────────
def test_factor_to_label_known():
    assert inference.factor_to_label("BMI") == "Indeks Massa Tubuh (BMI)"
    assert inference.factor_to_label("AgeCategory") == "Usia"


def test_factor_to_label_unknown_passthrough():
    assert inference.factor_to_label("XyzFeature") == "XyzFeature"
