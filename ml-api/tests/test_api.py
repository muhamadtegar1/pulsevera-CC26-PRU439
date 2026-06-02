"""Test main.py: compute_lifestyle_score + endpoint FastAPI via TestClient.
Model di-mock (conftest), Gemini dimatikan -> recommendation_source=rule_based."""
from __future__ import annotations

import pytest

import main


# ── compute_lifestyle_score (primary metric, inversi dari LifestyleRiskScore) ──
def test_lifestyle_perfect_score():
    ls = main.compute_lifestyle_score({
        "sex": "Male", "smoker_status": "Never", "physical_activities": "Yes",
        "sleep_hours": 7, "alcohol": "No", "height_meters": 1.70, "weight_kg": 70})
    assert ls.score == 5
    assert ls.grade == "Sangat Sehat"
    assert len(ls.habits) == 5
    assert all(h.good for h in ls.habits)


def test_lifestyle_worst_score():
    ls = main.compute_lifestyle_score({
        "sex": "Male", "smoker_status": "Current-every", "physical_activities": "No",
        "sleep_hours": 4, "alcohol": "Yes", "height_meters": 1.70, "weight_kg": 100})
    assert ls.score == 0
    assert ls.grade == "Berisiko Tinggi"
    assert all(not h.good for h in ls.habits)


def test_lifestyle_former_smoker_counts_as_good():
    ls = main.compute_lifestyle_score({
        "smoker_status": "Former", "physical_activities": "Yes", "sleep_hours": 7,
        "alcohol": "No", "height_meters": 1.70, "weight_kg": 70})
    smoking = next(h for h in ls.habits if h.key == "not_smoking")
    assert smoking.good is True


@pytest.mark.parametrize("sleep,good", [(5.9, False), (6, True), (9, True), (9.1, False)])
def test_lifestyle_sleep_boundaries(sleep, good):
    ls = main.compute_lifestyle_score({
        "smoker_status": "Never", "physical_activities": "Yes", "sleep_hours": sleep,
        "alcohol": "No", "height_meters": 1.70, "weight_kg": 70})
    assert next(h for h in ls.habits if h.key == "enough_sleep").good is good


@pytest.mark.parametrize("weight,good", [(53.5, True), (87.0, False)])  # BMI ~18.5 vs ~30 @1.70m
def test_lifestyle_bmi_boundaries(weight, good):
    ls = main.compute_lifestyle_score({
        "smoker_status": "Never", "physical_activities": "Yes", "sleep_hours": 7,
        "alcohol": "No", "height_meters": 1.70, "weight_kg": weight})
    assert next(h for h in ls.habits if h.key == "healthy_weight").good is good


def test_lifestyle_grade_map_covers_all_scores():
    """Tiap kombinasi 0..5 punya grade -> cegah KeyError."""
    seen = set()
    for w in (70, 100):
        for smoke in ("Never", "Current-every"):
            for act in ("Yes", "No"):
                for sl in (7, 4):
                    for alc in ("No", "Yes"):
                        ls = main.compute_lifestyle_score({
                            "smoker_status": smoke, "physical_activities": act,
                            "sleep_hours": sl, "alcohol": alc,
                            "height_meters": 1.70, "weight_kg": w})
                        seen.add(ls.score)
                        assert isinstance(ls.grade, str) and ls.grade
    assert seen == {0, 1, 2, 3, 4, 5}


# ── Endpoint: /health ─────────────────────────────────────────────────
def test_health_endpoint(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["model_loaded"] is True
    assert body["dl_model_loaded"] is True
    assert "gemini_recommendations" in body


def test_root_endpoint(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["service"] == "Pulsevera ML API"


# ── Endpoint: /api/v1/predict (DL) ────────────────────────────────────
def test_predict_happy_path_schema(client, valid_payload):
    r = client.post("/api/v1/predict", json=valid_payload)
    assert r.status_code == 200
    body = r.json()
    assert 0.0 <= body["risk_score"] <= 1.0
    assert body["risk_percent"] == pytest.approx(body["risk_score"] * 100, abs=0.5)
    assert body["risk_label"] in ("Rendah", "Sedang", "Tinggi")
    assert body["lifestyle"]["max_score"] == 5
    assert len(body["lifestyle"]["habits"]) == 5
    assert len(body["top_risk_factors"]) == 3
    assert all("feature" in f and "label" in f for f in body["top_risk_factors"])
    assert len(body["recommendations"]) > 0
    assert body["recommendation_source"] == "rule_based"  # Gemini off
    assert body["inference_ms"] >= 0


def test_predict_ml_endpoint(client, valid_payload):
    r = client.post("/api/v1/predict-ml", json=valid_payload)
    assert r.status_code == 200
    assert r.json()["risk_label"] in ("Rendah", "Sedang", "Tinggi")


@pytest.mark.parametrize("field,value", [
    ("age_category", 14),
    ("height_meters", 3.0),
    ("weight_kg", 500),
    ("sleep_hours", 99),
])
def test_predict_pydantic_validation_422(client, valid_payload, field, value):
    valid_payload[field] = value
    r = client.post("/api/v1/predict", json=valid_payload)
    assert r.status_code == 422


def test_predict_missing_field_422(client, valid_payload):
    del valid_payload["sex"]
    r = client.post("/api/v1/predict", json=valid_payload)
    assert r.status_code == 422


def test_predict_model_not_loaded_503(client, valid_payload, loaded_bundle):
    """DL model None -> 503 dengan pesan train.py."""
    loaded_bundle.dl_model = None
    r = client.post("/api/v1/predict", json=valid_payload)
    assert r.status_code == 503
    assert "train.py" in r.json()["detail"]
