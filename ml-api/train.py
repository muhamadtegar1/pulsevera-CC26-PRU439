"""
Pulsevera — Standalone Training Pipeline
End-to-end pipeline: load data DS -> train ML (LR/RF/DT) + DL -> simpan model untuk FastAPI.

Jalankan setelah download data:
    cd ml-api
    python train.py                    # ML + DL + SHAP
    python train.py --skip-dl          # ML + SHAP only
    python train.py --skip-shap        # tanpa SHAP

Output ke ml-api/models/:
    pulsevera_ml_model.pkl
    pulsevera_dl_model.keras
    scaler.pkl
    feature_metadata.json
    dl_metadata.json
    shap_explainer.pkl
    ml_results.json
"""
from __future__ import annotations

import argparse
import json
import logging
import time
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger('train')

BASE_DIR = Path(__file__).resolve().parent.parent
FINAL_DIR = BASE_DIR / 'data' / 'final'
MODELS_DIR = Path(__file__).parent / 'models'
LOG_DIR = Path(__file__).parent / 'tensorboard_logs'

RANDOM_STATE = 42


def load_data():
    if not FINAL_DIR.exists():
        raise FileNotFoundError(
            f'{FINAL_DIR} tidak ditemukan. Download dataset dari Google Drive '
            '(lihat README) dan letakkan di data/final/.'
        )
    X_train = pd.read_csv(FINAL_DIR / 'X_train.csv')
    X_test = pd.read_csv(FINAL_DIR / 'X_test.csv')
    y_train = pd.read_csv(FINAL_DIR / 'y_train.csv').squeeze()
    y_test = pd.read_csv(FINAL_DIR / 'y_test.csv').squeeze()
    log.info('Data loaded — X_train=%s, X_test=%s', X_train.shape, X_test.shape)
    return X_train, X_test, y_train, y_test


def train_ml(X_train, X_test, y_train, y_test, do_tune: bool = True):
    from imblearn.over_sampling import SMOTE
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import (
        accuracy_score, f1_score, precision_score, recall_score, roc_auc_score,
    )
    from sklearn.model_selection import RandomizedSearchCV
    from sklearn.preprocessing import StandardScaler
    from sklearn.tree import DecisionTreeClassifier

    log.info('Apply SMOTE (sampling_strategy=0.3)...')
    smote = SMOTE(random_state=RANDOM_STATE, sampling_strategy=0.3)
    X_res, y_res = smote.fit_resample(X_train, y_train)
    log.info('After SMOTE: %s | positif=%d', X_res.shape, int(np.sum(y_res == 1)))

    scaler = StandardScaler().fit(X_res)
    X_res_s = scaler.transform(X_res)
    X_test_s = scaler.transform(X_test)
    joblib.dump(scaler, MODELS_DIR / 'scaler.pkl')

    def metrics(name, y_t, y_p, y_pr, secs):
        return {
            'model': name,
            'accuracy': float(accuracy_score(y_t, y_p)),
            'precision_pos': float(precision_score(y_t, y_p, pos_label=1, zero_division=0)),
            'recall_pos': float(recall_score(y_t, y_p, pos_label=1, zero_division=0)),
            'f1_pos': float(f1_score(y_t, y_p, pos_label=1, zero_division=0)),
            'roc_auc': float(roc_auc_score(y_t, y_pr)),
            'train_seconds': round(secs, 2),
        }

    results = {}
    candidates = {}

    log.info('Train Logistic Regression...')
    t0 = time.time()
    lr = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=RANDOM_STATE, n_jobs=-1)
    lr.fit(X_res_s, y_res)
    y_pred = lr.predict(X_test_s)
    y_pr = lr.predict_proba(X_test_s)[:, 1]
    results['Logistic Regression'] = metrics('Logistic Regression', y_test, y_pred, y_pr, time.time() - t0)
    candidates['Logistic Regression'] = (lr, True)

    log.info('Train Decision Tree...')
    t0 = time.time()
    dt = DecisionTreeClassifier(max_depth=12, class_weight='balanced', random_state=RANDOM_STATE)
    dt.fit(X_res, y_res)
    y_pred = dt.predict(X_test)
    y_pr = dt.predict_proba(X_test)[:, 1]
    results['Decision Tree'] = metrics('Decision Tree', y_test, y_pred, y_pr, time.time() - t0)
    candidates['Decision Tree'] = (dt, False)

    log.info('Train Random Forest (baseline)...')
    t0 = time.time()
    rf = RandomForestClassifier(
        n_estimators=200, max_depth=20, min_samples_split=5,
        class_weight='balanced', random_state=RANDOM_STATE, n_jobs=-1,
    )
    rf.fit(X_res, y_res)
    y_pred = rf.predict(X_test)
    y_pr = rf.predict_proba(X_test)[:, 1]
    results['Random Forest'] = metrics('Random Forest', y_test, y_pred, y_pr, time.time() - t0)
    candidates['Random Forest'] = (rf, False)

    if do_tune:
        log.info('Hyperparameter tuning Random Forest (15 iter, 3-fold CV)...')
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 15, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'class_weight': ['balanced', 'balanced_subsample'],
        }
        t0 = time.time()
        search = RandomizedSearchCV(
            RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1),
            param_distributions=param_grid, n_iter=15, cv=3,
            scoring='f1', random_state=RANDOM_STATE, n_jobs=-1, verbose=1,
        )
        search.fit(X_res, y_res)
        rf_tuned = search.best_estimator_
        y_pred = rf_tuned.predict(X_test)
        y_pr = rf_tuned.predict_proba(X_test)[:, 1]
        results['Random Forest (tuned)'] = metrics('Random Forest (tuned)', y_test, y_pred, y_pr, time.time() - t0)
        results['Random Forest (tuned)']['best_params'] = search.best_params_
        candidates['Random Forest (tuned)'] = (rf_tuned, False)

    best_name = max(candidates, key=lambda k: results[k]['f1_pos'])
    best_model, needs_scaling = candidates[best_name]
    log.info('Best ML: %s | f1_pos=%.4f', best_name, results[best_name]['f1_pos'])

    joblib.dump(best_model, MODELS_DIR / 'pulsevera_ml_model.pkl')

    feature_meta = {
        'feature_order': X_train.columns.tolist(),
        'n_features': X_train.shape[1],
        'best_model_name': best_name,
        'needs_scaling': bool(needs_scaling),
        'feature_means': X_train.mean().round(4).to_dict(),
        'feature_medians': X_train.median().round(4).to_dict(),
        'trained_at': datetime.utcnow().isoformat() + 'Z',
    }
    with open(MODELS_DIR / 'feature_metadata.json', 'w') as f:
        json.dump(feature_meta, f, indent=2)
    with open(MODELS_DIR / 'ml_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=float)
    return best_model, scaler, feature_meta, results


def train_dl(X_train, X_test, y_train, y_test, scaler, epochs: int = 30, use_smote: bool = True):
    import tensorflow as tf
    import keras
    from keras import layers
    from imblearn.over_sampling import SMOTE
    from sklearn.metrics import (
        accuracy_score, f1_score, precision_score, recall_score, roc_auc_score,
    )
    from sklearn.utils.class_weight import compute_class_weight

    np.random.seed(RANDOM_STATE)
    tf.random.set_seed(RANDOM_STATE)

    if use_smote:
        log.info('Apply SMOTE for DL training (sampling_strategy=0.3)...')
        smote = SMOTE(random_state=RANDOM_STATE, sampling_strategy=0.3)
        X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
        log.info('After SMOTE: %s | positif=%d',
                 X_train_res.shape, int(np.sum(y_train_res == 1)))
    else:
        log.info('SMOTE disabled for DL (notebook 06 style: class_weight only)...')
        X_train_res, y_train_res = X_train, y_train

    X_train_s = scaler.transform(X_train_res).astype('float32')
    X_test_s = scaler.transform(X_test).astype('float32')
    y_train_arr = y_train_res.values.astype('float32') if hasattr(y_train_res, 'values') else np.asarray(y_train_res, dtype='float32')
    y_test_arr = y_test.values.astype('float32')

    @keras.saving.register_keras_serializable(package='pulsevera', name='focal_loss')
    def focal_loss(y_true, y_pred, gamma=2.0, alpha=0.25):
        y_true = tf.cast(y_true, tf.float32)
        y_pred = tf.clip_by_value(y_pred, 1e-7, 1 - 1e-7)
        bce = -(y_true * tf.math.log(y_pred) + (1 - y_true) * tf.math.log(1 - y_pred))
        p_t = y_true * y_pred + (1 - y_true) * (1 - y_pred)
        alpha_t = y_true * alpha + (1 - y_true) * (1 - alpha)
        return tf.reduce_mean(alpha_t * tf.pow(1.0 - p_t, gamma) * bce)

    class EarlyStoppingByRecall(keras.callbacks.Callback):
        def __init__(self, patience=5, monitor='val_recall'):
            super().__init__()
            self.patience = patience
            self.monitor = monitor
            self.best = -np.inf
            self.wait = 0
            self.best_weights = None

        def on_epoch_end(self, epoch, logs=None):
            current = (logs or {}).get(self.monitor)
            if current is None:
                return
            if current - self.best > 1e-3:
                self.best = current
                self.wait = 0
                self.best_weights = self.model.get_weights()
            else:
                self.wait += 1
                if self.wait >= self.patience:
                    self.model.stop_training = True
                    if self.best_weights is not None:
                        self.model.set_weights(self.best_weights)

    inputs = keras.Input(shape=(X_train_s.shape[1],), name='lifestyle_input')
    x = layers.Dense(256, activation='relu', kernel_initializer='he_normal')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(128, activation='relu', kernel_initializer='he_normal')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(64, activation='relu', kernel_initializer='he_normal')(x)
    x = layers.Dropout(0.15)(x)
    outputs = layers.Dense(1, activation='sigmoid', name='heart_attack_risk')(x)
    model = keras.Model(inputs=inputs, outputs=outputs, name='pulsevera_dl_model')

    cw = compute_class_weight('balanced', classes=np.array([0, 1]), y=y_train_arr)
    class_weight = {0: float(cw[0]), 1: float(cw[1])}

    model.compile(
        optimizer=keras.optimizers.Adam(1e-3),
        loss=focal_loss,
        metrics=[
            keras.metrics.BinaryAccuracy(name='accuracy'),
            keras.metrics.Recall(name='recall'),
            keras.metrics.Precision(name='precision'),
            keras.metrics.AUC(name='auc'),
        ],
    )

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    run_name = datetime.now().strftime('run_%Y%m%d_%H%M%S')
    run_dir = LOG_DIR / run_name

    log.info('Train DL (functional API) for up to %d epochs...', epochs)
    # Match notebook 06 Fathan exactly:
    # - validation_split=0.20 (bukan 0.15)
    # - TANPA ReduceLROnPlateau — LR diturunkan terlalu cepat menyebabkan
    #   model stuck di local minimum (all-negative) saat class imbalance ekstrem
    model.fit(
        X_train_s, y_train_arr,
        validation_split=0.20, epochs=epochs, batch_size=512,
        class_weight=class_weight,
        callbacks=[
            EarlyStoppingByRecall(patience=10),
            keras.callbacks.TensorBoard(log_dir=str(run_dir), histogram_freq=1),
        ],
        verbose=2,
    )

    y_proba = model.predict(X_test_s, batch_size=1024, verbose=0).ravel()

    # Comprehensive threshold tuning: prioritize recall >= 0.70 (medical priority)
    # then within recall-passing thresholds, pick the one with best F1
    threshold_candidates = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
    threshold_metrics = []
    for thr in threshold_candidates:
        y_pred_thr = (y_proba >= thr).astype(int)
        threshold_metrics.append({
            'threshold': thr,
            'recall': recall_score(y_test_arr, y_pred_thr, pos_label=1, zero_division=0),
            'precision': precision_score(y_test_arr, y_pred_thr, pos_label=1, zero_division=0),
            'f1': f1_score(y_test_arr, y_pred_thr, pos_label=1, zero_division=0),
            'accuracy': accuracy_score(y_test_arr, y_pred_thr),
        })

    # Pilih threshold yang capai recall >= 0.70 dengan F1 tertinggi
    recall_passing = [m for m in threshold_metrics if m['recall'] >= 0.70]
    if recall_passing:
        best = max(recall_passing, key=lambda m: m['f1'])
    else:
        # Tidak ada yang capai recall 0.70 → ambil yang recall paling tinggi
        best = max(threshold_metrics, key=lambda m: m['recall'])
        log.warning('Tidak ada threshold dengan recall >= 0.70. Pakai threshold dengan recall tertinggi: %.4f', best['recall'])

    best_thr = best['threshold']
    log.info('Best threshold: %.2f | recall=%.4f | precision=%.4f | f1=%.4f',
             best_thr, best['recall'], best['precision'], best['f1'])

    y_pred = (y_proba >= best_thr).astype(int)

    model.save(MODELS_DIR / 'pulsevera_dl_model.keras')
    dl_meta = {
        'framework': 'tensorflow',
        'tf_version': tf.__version__,
        'architecture': 'Dense[256-128-64-1] + BN + Dropout',
        'custom_components': ['focal_loss', 'EarlyStoppingByRecall'],
        'best_threshold': float(best_thr),
        'test_accuracy': float(accuracy_score(y_test_arr, y_pred)),
        'test_recall_pos': float(recall_score(y_test_arr, y_pred, pos_label=1, zero_division=0)),
        'test_precision_pos': float(precision_score(y_test_arr, y_pred, pos_label=1, zero_division=0)),
        'test_f1_pos': float(f1_score(y_test_arr, y_pred, pos_label=1, zero_division=0)),
        'test_roc_auc': float(roc_auc_score(y_test_arr, y_proba)),
        'class_weight': class_weight,
        'tensorboard_log_dir': str(run_dir),
    }
    with open(MODELS_DIR / 'dl_metadata.json', 'w') as f:
        json.dump(dl_meta, f, indent=2)
    log.info('DL saved | f1_pos=%.4f | recall_pos=%.4f',
             dl_meta['test_f1_pos'], dl_meta['test_recall_pos'])
    return model, dl_meta


def build_shap(ml_model, X_train, scaler, feature_meta, sample_size: int = 2000):
    import shap

    log.info('Build SHAP explainer (sample %d)...', sample_size)
    if hasattr(ml_model, 'estimators_'):
        explainer = shap.TreeExplainer(ml_model)
    elif hasattr(ml_model, 'coef_'):
        bg = X_train.sample(min(500, len(X_train)), random_state=RANDOM_STATE)
        bg_in = scaler.transform(bg) if feature_meta['needs_scaling'] else bg.values
        explainer = shap.LinearExplainer(
            ml_model, bg_in, feature_names=feature_meta['feature_order'],
        )
    else:
        bg = shap.sample(X_train, 100, random_state=RANDOM_STATE)
        explainer = shap.KernelExplainer(lambda d: ml_model.predict_proba(d)[:, 1], bg)

    try:
        joblib.dump(explainer, MODELS_DIR / 'shap_explainer.pkl')
        log.info('SHAP explainer saved.')
    except Exception as exc:
        log.warning('Tidak bisa serialize explainer (%s) — FastAPI akan rebuild on-demand.', exc)

    sample_idx = np.random.RandomState(RANDOM_STATE).choice(
        len(X_train), size=min(sample_size, len(X_train)), replace=False,
    )
    X_shap = X_train.iloc[sample_idx]
    X_shap_in = scaler.transform(X_shap) if feature_meta['needs_scaling'] else X_shap.values
    sv = explainer.shap_values(X_shap_in)
    if isinstance(sv, list):
        sv = sv[1] if len(sv) > 1 else sv[0]
    arr = np.asarray(sv)
    if arr.ndim == 3:
        arr = arr[:, :, 1]
    top = pd.Series(np.abs(arr).mean(axis=0), index=feature_meta['feature_order']).nlargest(10)
    with open(MODELS_DIR / 'shap_metadata.json', 'w') as f:
        json.dump({
            'explainer_type': type(explainer).__name__,
            'global_importance_top10': top.round(4).to_dict(),
        }, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Pulsevera training pipeline')
    parser.add_argument('--skip-ml', action='store_true')
    parser.add_argument('--skip-dl', action='store_true')
    parser.add_argument('--skip-shap', action='store_true')
    parser.add_argument('--no-tune', action='store_true', help='Skip RandomizedSearchCV')
    parser.add_argument('--no-smote-dl', action='store_true', help='Disable SMOTE for DL training (use class_weight only — notebook 06 Fathan style)')
    parser.add_argument('--epochs', type=int, default=30)
    args = parser.parse_args()

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    X_train, X_test, y_train, y_test = load_data()

    ml_model = None
    scaler = None
    feature_meta = None

    if not args.skip_ml:
        ml_model, scaler, feature_meta, _ = train_ml(
            X_train, X_test, y_train, y_test, do_tune=not args.no_tune,
        )
    else:
        scaler_path = MODELS_DIR / 'scaler.pkl'
        meta_path = MODELS_DIR / 'feature_metadata.json'
        if scaler_path.exists() and meta_path.exists():
            scaler = joblib.load(scaler_path)
            with open(meta_path) as f:
                feature_meta = json.load(f)
            ml_model = joblib.load(MODELS_DIR / 'pulsevera_ml_model.pkl')

    if not args.skip_dl:
        if scaler is None:
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler().fit(X_train)
            joblib.dump(scaler, MODELS_DIR / 'scaler.pkl')
        train_dl(X_train, X_test, y_train, y_test, scaler, epochs=args.epochs, use_smote=not args.no_smote_dl)

    if not args.skip_shap and ml_model is not None and feature_meta is not None:
        build_shap(ml_model, X_train, scaler, feature_meta)

    log.info('Training pipeline selesai. Output di %s', MODELS_DIR)


if __name__ == '__main__':
    main()
