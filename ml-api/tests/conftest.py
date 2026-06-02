"""Shared fixtures. Dummy model bundle supaya test tidak butuh TensorFlow
atau file .keras asli — deterministik & cepat di CI."""
from __future__ import annotations

import numpy as np
import pytest
from fastapi.testclient import TestClient

import inference
import main
import preprocessing


class FakeDLModel:
    """Mengembalikan probabilitas tetap, meniru keras model.predict()."""

    def __init__(self, proba: float = 0.30) -> None:
        self.proba = proba

    def predict(self, X, verbose=0):  # noqa: N803
        n = X.shape[0]
        return np.full((n, 1), self.proba, dtype="float32")


class FakeMLModel:
    """Meniru RandomForest: predict_proba + feature_importances_."""

    def __init__(self, n_features: int, proba: float = 0.30) -> None:
        self.proba = proba
        # importance menurun supaya urutan deterministik
        self.feature_importances_ = np.linspace(1.0, 0.1, n_features)

    def predict_proba(self, X):  # noqa: N803
        n = X.shape[0]
        return np.tile([1 - self.proba, self.proba], (n, 1))


@pytest.fixture
def feature_order():
    return preprocessing.get_feature_order()


@pytest.fixture
def valid_payload():
    """Profil user lengkap & valid (10 field web form)."""
    return {
        "sex": "Male",
        "age_category": 7,
        "height_meters": 1.70,
        "weight_kg": 70.0,
        "sleep_hours": 7.0,
        "physical_activities": "Yes",
        "smoker_status": "Never",
        "alcohol": "No",
        "general_health": "Good",
        "diabetes": "No",
    }


@pytest.fixture
def loaded_bundle(monkeypatch, feature_order):
    """Pasang fake model ke inference.bundle, kembalikan setelah test."""
    b = inference.bundle
    saved = (b.ml_model, b.dl_model, b.scaler, b.feature_order, b.feature_meta, b.dl_meta)

    b.ml_model = FakeMLModel(len(feature_order))
    b.dl_model = FakeDLModel(proba=0.30)
    b.scaler = None
    b.feature_order = feature_order
    b.feature_meta = {"best_model_name": "RandomForest(test)", "needs_scaling": False}
    b.dl_meta = {"architecture": "MLP(test)"}

    yield b

    (b.ml_model, b.dl_model, b.scaler, b.feature_order, b.feature_meta, b.dl_meta) = saved


@pytest.fixture
def client(loaded_bundle, monkeypatch):
    """TestClient dengan model dummy & Gemini dimatikan (fallback rule_based)."""
    monkeypatch.setattr(main, "gemini_client", None)
    # TestClient tanpa context manager -> startup tidak reload model asli.
    return TestClient(main.app)
