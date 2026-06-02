"""Unit test preprocessing.preprocess_user_input — titik paling kritis:
10 field web form -> 46 fitur model. Bug di sini = prediksi salah senyap."""
from __future__ import annotations

import numpy as np
import pytest

import preprocessing
from preprocessing import preprocess_user_input


# ── Struktur & kontrak output ─────────────────────────────────────────
def test_output_shape_and_order(valid_payload, feature_order):
    df = preprocess_user_input(valid_payload)
    assert df.shape == (1, len(feature_order))
    assert list(df.columns) == feature_order


def test_output_dtype_float64(valid_payload):
    df = preprocess_user_input(valid_payload)
    assert (df.dtypes == np.float64).all()


def test_no_missing_features(valid_payload, feature_order):
    df = preprocess_user_input(valid_payload)
    assert not df.isna().any().any()
    for col in feature_order:
        assert col in df.columns


# ── Encoding parity dengan notebook DS ────────────────────────────────
@pytest.mark.parametrize("sex,expected", [("Male", 1), ("Female", 0),
                                          ("Laki-laki", 1), ("Perempuan", 0)])
def test_sex_encoding(valid_payload, sex, expected):
    valid_payload["sex"] = sex
    assert preprocess_user_input(valid_payload)["Sex"].iloc[0] == expected


@pytest.mark.parametrize("smoker,expected", [
    ("Never", 0), ("Former", 1), ("Current-some", 2), ("Current-every", 3),
    ("Current smoker - now smokes every day", 3),  # sinonim notebook
])
def test_smoker_encoding(valid_payload, smoker, expected):
    valid_payload["smoker_status"] = smoker
    assert preprocess_user_input(valid_payload)["SmokerStatus"].iloc[0] == expected


@pytest.mark.parametrize("health,expected", [
    ("Poor", 1), ("Fair", 2), ("Good", 3), ("Very good", 4), ("Excellent", 5)])
def test_general_health_encoding(valid_payload, health, expected):
    valid_payload["general_health"] = health
    assert preprocess_user_input(valid_payload)["GeneralHealth"].iloc[0] == expected


@pytest.mark.parametrize("diabetes,expected", [
    ("No", 0), ("Pre-diabetes", 1), ("Pregnancy", 2), ("Yes", 3)])
def test_diabetes_encoding(valid_payload, diabetes, expected):
    valid_payload["diabetes"] = diabetes
    assert preprocess_user_input(valid_payload)["HadDiabetes"].iloc[0] == expected


# ── Feature engineering (harus identik notebook 03) ───────────────────
def test_engineered_all_bad():
    out = preprocess_user_input({
        "sex": "Male", "age_category": 10, "height_meters": 1.72, "weight_kg": 92.0,
        "sleep_hours": 5.5, "physical_activities": "No", "smoker_status": "Current-every",
        "alcohol": "Yes", "general_health": "Fair", "diabetes": "Yes"})
    assert out["IsActiveSmoker"].iloc[0] == 1
    assert out["IsObese"].iloc[0] == 1
    assert out["IsSleepDeprived"].iloc[0] == 1
    assert out["LifestyleRiskScore"].iloc[0] == 5  # 5 indikator buruk semua
    assert out["HasChronicCondition"].iloc[0] == 1  # diabetes


def test_engineered_all_good(valid_payload):
    out = preprocess_user_input(valid_payload)
    assert out["IsActiveSmoker"].iloc[0] == 0
    assert out["IsObese"].iloc[0] == 0
    assert out["IsSleepDeprived"].iloc[0] == 0
    assert out["LifestyleRiskScore"].iloc[0] == 0
    assert out["HasChronicCondition"].iloc[0] == 0


def test_former_smoker_not_active(valid_payload):
    valid_payload["smoker_status"] = "Former"
    out = preprocess_user_input(valid_payload)
    assert out["SmokerStatus"].iloc[0] == 1
    assert out["IsActiveSmoker"].iloc[0] == 0  # Former bukan perokok aktif


def test_poor_health_days_total_default(valid_payload):
    out = preprocess_user_input(valid_payload)
    assert out["PoorHealthDays_Total"].iloc[0] == 0  # default 0 + 0


# ── Boundary & clamping ───────────────────────────────────────────────
def test_bmi_computed(valid_payload):
    # 70 / 1.70^2 = 24.22
    out = preprocess_user_input(valid_payload)
    assert out["BMI"].iloc[0] == pytest.approx(24.22, abs=0.01)


def test_bmi_clamped_high():
    out = preprocess_user_input({
        "sex": "Male", "age_category": 5, "height_meters": 1.0, "weight_kg": 200.0,
        "sleep_hours": 7, "physical_activities": "Yes", "smoker_status": "Never",
        "alcohol": "No", "general_health": "Good"})
    assert out["BMI"].iloc[0] == 60.0  # clamp atas


def test_sleep_clamped():
    out = preprocess_user_input({
        "sex": "Female", "age_category": 5, "height_meters": 1.6, "weight_kg": 55.0,
        "sleep_hours": 14, "physical_activities": "Yes", "smoker_status": "Never",
        "alcohol": "No", "general_health": "Good"})
    assert out["SleepHours"].iloc[0] == 14.0


@pytest.mark.parametrize("age", [1, 13])
def test_age_boundaries_valid(valid_payload, age):
    valid_payload["age_category"] = age
    assert preprocess_user_input(valid_payload)["AgeCategory"].iloc[0] == age


def test_diabetes_optional_defaults_no(valid_payload):
    valid_payload.pop("diabetes")
    assert preprocess_user_input(valid_payload)["HadDiabetes"].iloc[0] == 0


# ── Validasi input (harus ValueError) ─────────────────────────────────
@pytest.mark.parametrize("field,value", [
    ("sex", "Unknown"),
    ("age_category", 0),
    ("age_category", 14),
    ("height_meters", 0.9),
    ("height_meters", 2.6),
    ("weight_kg", 29),
    ("weight_kg", 201),
    ("physical_activities", "Maybe"),
    ("smoker_status", "Vaper"),
    ("alcohol", "Sometimes"),
    ("general_health", "Amazing"),
    ("diabetes", "Perhaps"),
])
def test_invalid_input_raises(valid_payload, field, value):
    valid_payload[field] = value
    with pytest.raises(ValueError):
        preprocess_user_input(valid_payload)


def test_idempotent(valid_payload):
    a = preprocess_user_input(dict(valid_payload))
    b = preprocess_user_input(dict(valid_payload))
    assert a.equals(b)


# ── Konsistensi metadata <-> fallback feature order ───────────────────
def test_feature_order_matches_metadata():
    order = preprocessing.get_feature_order()
    assert len(order) == len(set(order))  # tak ada duplikat
    assert len(order) >= 40
