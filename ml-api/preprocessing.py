"""
Pulsevera — Preprocessing Pipeline
Konversi 10 field input web form menjadi 46 fitur yang dibutuhkan model.

Encoding mapping konsisten dengan notebooks/01_data_wrangling.ipynb dan
notebooks/03_feature_engineering.ipynb (Data Scientist).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


# ── Mapping konstanta (harus identik dengan pipeline DS) ──────────────
SEX_MAP = {'Male': 1, 'Female': 0, 'Laki-laki': 1, 'Perempuan': 0}

SMOKER_MAP = {
    'Never': 0,
    'Former': 1,
    'Current-some': 2,
    'Current-every': 3,
    # Sinonim dari notebook DS:
    'Never smoked': 0,
    'Former smoker': 1,
    'Current smoker - now smokes some days': 2,
    'Current smoker - now smokes every day': 3,
}

GENERAL_HEALTH_MAP = {
    'Poor': 1,
    'Fair': 2,
    'Good': 3,
    'Very good': 4,
    'Excellent': 5,
}

DIABETES_MAP = {
    'No': 0,
    'Pre-diabetes': 1,
    'Pregnancy': 2,
    'Yes': 3,
    'No, pre-diabetes or borderline diabetes': 1,
    'Yes, but female told only during pregnancy': 2,
}

YES_NO_MAP = {'Yes': 1, 'No': 0, 'Ya': 1, 'Tidak': 0}


# ── Default values untuk 36 fitur yang tidak ditanyakan ke user ─────
# Nilai diturunkan dari distribusi populasi di X_train (median/mode)
DEFAULT_VALUES: dict[str, float | int] = {
    # Kesehatan umum
    'PhysicalHealthDays': 0.0,
    'MentalHealthDays': 0.0,
    'LastCheckupTime': 0,
    'RemovedTeeth': 0,
    # Riwayat penyakit kardiovaskular
    'HadAngina': 0,
    'HadStroke': 0,
    # Riwayat penyakit kronis
    'HadAsthma': 0,
    'HadCOPD': 0,
    'HadKidneyDisease': 0,
    'HadArthritis': 0,
    'HadSkinCancer': 0,
    'HadDepressiveDisorder': 0,
    # Disabilitas
    'DeafOrHardOfHearing': 0,
    'BlindOrVisionDifficulty': 0,
    'DifficultyConcentrating': 0,
    'DifficultyWalking': 0,
    'DifficultyDressingBathing': 0,
    'DifficultyErrands': 0,
    # Pencegahan & screening
    'ChestScan': 0,
    'FluVaxLast12': 1,
    'HIVTesting': 0,
    'CovidPos': 0,
    'HighRiskLastYear': 0,
    'ECigaretteUsage': 0,
    # Ras (default white only — terbesar di dataset US)
    'Race_Black only, Non-Hispanic': 0,
    'Race_Hispanic': 0,
    'Race_Multiracial, Non-Hispanic': 0,
    'Race_Other race only, Non-Hispanic': 0,
    'Race_White only, Non-Hispanic': 1,
}


# ── Util ──────────────────────────────────────────────────────────────
def _load_feature_metadata() -> dict:
    """Load FEATURE_ORDER dari metadata yang disimpan training."""
    meta_path = Path(__file__).parent / 'models' / 'feature_metadata.json'
    if meta_path.exists():
        with open(meta_path) as f:
            return json.load(f)
    return {}


def get_feature_order() -> list[str]:
    """Urutan kolom yang dipakai model. Jatuhkan ke default bila metadata belum ada."""
    meta = _load_feature_metadata()
    if 'feature_order' in meta:
        return meta['feature_order']
    return [
        'Sex', 'GeneralHealth', 'PhysicalHealthDays', 'MentalHealthDays', 'LastCheckupTime',
        'PhysicalActivities', 'SleepHours', 'RemovedTeeth', 'HadAngina', 'HadStroke',
        'HadAsthma', 'HadCOPD', 'HadKidneyDisease', 'HadArthritis', 'HadSkinCancer',
        'HadDepressiveDisorder', 'HadDiabetes', 'DeafOrHardOfHearing', 'BlindOrVisionDifficulty',
        'DifficultyConcentrating', 'DifficultyWalking', 'DifficultyDressingBathing', 'DifficultyErrands',
        'SmokerStatus', 'ECigaretteUsage', 'ChestScan', 'AgeCategory', 'HeightInMeters',
        'WeightInKilograms', 'BMI', 'AlcoholDrinkers', 'HIVTesting', 'FluVaxLast12',
        'CovidPos', 'HighRiskLastYear',
        'Race_Black only, Non-Hispanic', 'Race_Hispanic', 'Race_Multiracial, Non-Hispanic',
        'Race_Other race only, Non-Hispanic', 'Race_White only, Non-Hispanic',
        'IsActiveSmoker', 'IsObese', 'IsSleepDeprived',
        'LifestyleRiskScore', 'HasChronicCondition', 'PoorHealthDays_Total',
    ]


# ── Preprocessing utama ────────────────────────────────────────────────
def preprocess_user_input(user_input: dict) -> pd.DataFrame:
    """
    Konversi 10 field input user dari web form ke DataFrame 1 baris siap predict.

    Field yang diharapkan:
        sex                 : "Male" | "Female"
        age_category        : int 1..13  (1=18-24, ..., 13=80+)
        height_meters       : float 1.0..2.5
        weight_kg           : float 30..200
        sleep_hours         : float 1..14
        physical_activities : "Yes" | "No"
        smoker_status       : "Never" | "Former" | "Current-some" | "Current-every"
        alcohol             : "Yes" | "No"
        general_health      : "Poor" | "Fair" | "Good" | "Very good" | "Excellent"
        diabetes            : "No" | "Pre-diabetes" | "Yes"   (default "No")

    Return DataFrame[1 x len(FEATURE_ORDER)] berurutan sesuai training.
    """
    data: dict[str, float | int] = dict(DEFAULT_VALUES)

    # Demografis
    sex = user_input.get('sex')
    if sex not in SEX_MAP:
        raise ValueError(f"Sex '{sex}' tidak dikenali. Pakai 'Male' atau 'Female'.")
    data['Sex'] = SEX_MAP[sex]

    age = int(user_input.get('age_category', 0))
    if not 1 <= age <= 13:
        raise ValueError(f"age_category {age} di luar range 1..13.")
    data['AgeCategory'] = age

    # Antropometri
    height = float(user_input.get('height_meters', 0))
    weight = float(user_input.get('weight_kg', 0))
    if not 1.0 <= height <= 2.5:
        raise ValueError(f"height_meters {height} di luar range 1.0..2.5.")
    if not 30.0 <= weight <= 200.0:
        raise ValueError(f"weight_kg {weight} di luar range 30..200.")
    bmi = weight / (height ** 2)
    data['HeightInMeters'] = round(height, 2)
    data['WeightInKilograms'] = round(weight, 2)
    data['BMI'] = round(min(max(bmi, 13.0), 60.0), 2)

    # Gaya hidup
    sleep = float(user_input.get('sleep_hours', 7))
    data['SleepHours'] = max(1.0, min(14.0, sleep))

    phys = user_input.get('physical_activities', 'Yes')
    if phys not in YES_NO_MAP:
        raise ValueError(f"physical_activities '{phys}' invalid.")
    data['PhysicalActivities'] = YES_NO_MAP[phys]

    smoker = user_input.get('smoker_status', 'Never')
    if smoker not in SMOKER_MAP:
        raise ValueError(f"smoker_status '{smoker}' invalid.")
    data['SmokerStatus'] = SMOKER_MAP[smoker]

    alcohol = user_input.get('alcohol', 'No')
    if alcohol not in YES_NO_MAP:
        raise ValueError(f"alcohol '{alcohol}' invalid.")
    data['AlcoholDrinkers'] = YES_NO_MAP[alcohol]

    # Kesehatan umum
    health = user_input.get('general_health', 'Good')
    if health not in GENERAL_HEALTH_MAP:
        raise ValueError(f"general_health '{health}' invalid.")
    data['GeneralHealth'] = GENERAL_HEALTH_MAP[health]

    diabetes = user_input.get('diabetes', 'No')
    if diabetes not in DIABETES_MAP:
        raise ValueError(f"diabetes '{diabetes}' invalid.")
    data['HadDiabetes'] = DIABETES_MAP[diabetes]

    # ── Feature engineering (identik dengan notebook 03) ───────────
    data['IsActiveSmoker'] = 1 if data['SmokerStatus'] >= 2 else 0
    data['IsObese'] = 1 if data['BMI'] >= 30 else 0
    data['IsSleepDeprived'] = 1 if data['SleepHours'] < 6 else 0
    data['LifestyleRiskScore'] = int(
        data['IsActiveSmoker']
        + (1 - data['PhysicalActivities'])
        + data['AlcoholDrinkers']
        + data['IsSleepDeprived']
        + data['IsObese']
    )
    chronic = ['HadDiabetes', 'HadStroke', 'HadAsthma', 'HadCOPD', 'HadKidneyDisease']
    data['HasChronicCondition'] = 1 if any(data[c] > 0 for c in chronic) else 0
    data['PoorHealthDays_Total'] = data['PhysicalHealthDays'] + data['MentalHealthDays']

    # ── Susun sesuai FEATURE_ORDER ────────────────────────────────
    feature_order = get_feature_order()
    missing = [f for f in feature_order if f not in data]
    if missing:
        meta = _load_feature_metadata()
        medians = meta.get('feature_medians', {})
        for col in missing:
            data[col] = medians.get(col, 0)

    df = pd.DataFrame([data])[feature_order]
    return df.astype(np.float64)


# ── Self-test cepat (jalankan: python preprocessing.py) ───────────────
if __name__ == '__main__':
    demo = {
        'sex': 'Male', 'age_category': 10, 'height_meters': 1.72, 'weight_kg': 92.0,
        'sleep_hours': 5.5, 'physical_activities': 'No', 'smoker_status': 'Current-every',
        'alcohol': 'Yes', 'general_health': 'Fair', 'diabetes': 'Yes',
    }
    out = preprocess_user_input(demo)
    print(f'Shape: {out.shape}')
    print('Engineered features:')
    for c in ['BMI', 'IsActiveSmoker', 'IsObese', 'IsSleepDeprived',
              'LifestyleRiskScore', 'HasChronicCondition', 'PoorHealthDays_Total']:
        if c in out.columns:
            print(f'  {c:25s}: {out[c].iloc[0]}')
