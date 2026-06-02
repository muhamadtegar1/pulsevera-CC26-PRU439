"""
DL Architecture Experiments — Pulsevera P2-6

Train 6 variasi arsitektur DL pada data yang sama untuk justifikasi model selection.
Semua varian pakai SMOTE + Focal Loss + threshold 0.23.

Jalankan:
    cd ml-api
    python dl_experiments.py

Output:
    reports/dl_experiments.json              — metrics semua varian
    reports/dl_experiments_comparison.png    — bar chart comparison
"""
from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger('dl-experiments')

BASE_DIR = Path(__file__).resolve().parent.parent
FINAL_DIR = BASE_DIR / 'data' / 'final'
MODELS_DIR = Path(__file__).parent / 'models'
REPORTS_DIR = BASE_DIR / 'reports'
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
EPOCHS = 15          # Reduced untuk experiment (baseline pakai 30)
BATCH_SIZE = 512
THRESHOLD = 0.23     # Production threshold yang sudah dipilih

VARIANTS = [
    {
        'name': 'Baseline (Production)',
        'desc': 'Dense[256-128-64-1] + BN + Dropout 0.3',
        'layers': [256, 128, 64],
        'use_bn': True,
        'dropout_rates': [0.3, 0.3, 0.15],
        'final_dropout': False,
    },
    {
        'name': 'Shallow NN',
        'desc': 'Dense[64-1] + Dropout 0.3',
        'layers': [64],
        'use_bn': False,
        'dropout_rates': [0.3],
        'final_dropout': False,
    },
    {
        'name': 'Deep NN',
        'desc': 'Dense[512-256-128-64-32-1] + BN + Dropout 0.3',
        'layers': [512, 256, 128, 64, 32],
        'use_bn': True,
        'dropout_rates': [0.3, 0.3, 0.3, 0.3, 0.15],
        'final_dropout': False,
    },
    {
        'name': 'Wide NN',
        'desc': 'Dense[512-512-1] + BN + Dropout 0.3',
        'layers': [512, 512],
        'use_bn': True,
        'dropout_rates': [0.3, 0.3],
        'final_dropout': False,
    },
    {
        'name': 'No BatchNorm',
        'desc': 'Dense[256-128-64-1] + Dropout 0.3 (no BN)',
        'layers': [256, 128, 64],
        'use_bn': False,
        'dropout_rates': [0.3, 0.3, 0.15],
        'final_dropout': False,
    },
    {
        'name': 'No Final Dropout',
        'desc': 'Dense[256-128-64-1] + BN + Dropout (except before output)',
        'layers': [256, 128, 64],
        'use_bn': True,
        'dropout_rates': [0.3, 0.3, 0.0],
        'final_dropout': False,
    },
]


def load_data():
    X_train = pd.read_csv(FINAL_DIR / 'X_train.csv')
    X_test = pd.read_csv(FINAL_DIR / 'X_test.csv')
    y_train = pd.read_csv(FINAL_DIR / 'y_train.csv').squeeze()
    y_test = pd.read_csv(FINAL_DIR / 'y_test.csv').squeeze()
    bool_cols = X_train.select_dtypes(include='bool').columns
    X_train[bool_cols] = X_train[bool_cols].astype('float32')
    X_test[bool_cols] = X_test[bool_cols].astype('float32')
    return X_train, X_test, y_train, y_test


def build_variant(variant: dict, n_features: int):
    import re
    import keras
    from keras import layers

    safe_name = re.sub(r'[^A-Za-z0-9_.]', '_', variant['name'])

    inp = keras.Input(shape=(n_features,), name='input')
    x = inp
    for i, (units, dropout_rate) in enumerate(
        zip(variant['layers'], variant['dropout_rates'])
    ):
        x = layers.Dense(units, activation='relu', kernel_initializer='he_normal')(x)
        if variant['use_bn']:
            x = layers.BatchNormalization()(x)
        if dropout_rate > 0:
            x = layers.Dropout(dropout_rate)(x)
    out = layers.Dense(1, activation='sigmoid', name='output')(x)
    return keras.Model(inputs=inp, outputs=out, name=safe_name)


def focal_loss(y_true, y_pred, gamma=2.0, alpha=0.25):
    import tensorflow as tf
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.clip_by_value(y_pred, 1e-7, 1.0 - 1e-7)
    bce = -(y_true * tf.math.log(y_pred) + (1.0 - y_true) * tf.math.log(1.0 - y_pred))
    p_t = y_true * y_pred + (1.0 - y_true) * (1.0 - y_pred)
    alpha_t = y_true * alpha + (1.0 - y_true) * (1.0 - alpha)
    return tf.reduce_mean(alpha_t * tf.pow(1.0 - p_t, gamma) * bce)


def train_variant(variant: dict, X_train_s, y_train_arr, X_test_s, y_test_arr,
                  class_weight: dict) -> dict:
    import tensorflow as tf
    import keras
    keras.backend.clear_session()  # reset TF graph state antar variant

    tf.random.set_seed(RANDOM_STATE)
    np.random.seed(RANDOM_STATE)

    model = build_variant(variant, X_train_s.shape[1])
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

    class EarlyStoppingByRecall(keras.callbacks.Callback):
        def __init__(self, patience=5):
            super().__init__()
            self.patience = patience
            self.best = -np.inf
            self.wait = 0
            self.best_weights = None

        def on_epoch_end(self, epoch, logs=None):
            current = (logs or {}).get('val_recall', 0.0)
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

    t0 = time.time()
    model.fit(
        X_train_s, y_train_arr,
        validation_split=0.20,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        class_weight=class_weight,
        callbacks=[EarlyStoppingByRecall(patience=5)],
        verbose=0,
    )
    elapsed = time.time() - t0

    from sklearn.metrics import (
        accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
    )

    y_proba = model.predict(X_test_s, batch_size=1024, verbose=0).ravel()
    y_pred = (y_proba >= THRESHOLD).astype(int)

    n_params = int(model.count_params())
    return {
        'name': variant['name'],
        'desc': variant['desc'],
        'n_params': n_params,
        'train_seconds': round(elapsed, 1),
        'threshold': THRESHOLD,
        'accuracy': float(accuracy_score(y_test_arr, y_pred)),
        'recall': float(recall_score(y_test_arr, y_pred, pos_label=1, zero_division=0)),
        'precision': float(precision_score(y_test_arr, y_pred, pos_label=1, zero_division=0)),
        'f1': float(f1_score(y_test_arr, y_pred, pos_label=1, zero_division=0)),
        'roc_auc': float(roc_auc_score(y_test_arr, y_proba)),
    }


def plot_comparison(results: list[dict]) -> None:
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        names = [r['name'] for r in results]
        metrics = ['accuracy', 'recall', 'precision', 'f1', 'roc_auc']
        labels = ['Accuracy', 'Recall', 'Precision', 'F1', 'ROC-AUC']
        colors = ['#3b82f6', '#ef4444', '#f59e0b', '#10b981', '#8b5cf6']

        x = np.arange(len(names))
        width = 0.15
        fig, ax = plt.subplots(figsize=(14, 6))

        for i, (metric, label, color) in enumerate(zip(metrics, labels, colors)):
            vals = [r[metric] for r in results]
            bars = ax.bar(x + i * width, vals, width, label=label, color=color,
                          alpha=0.85, edgecolor='white')
            for bar, val in zip(bars, vals):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.002,
                        f'{val:.3f}', ha='center', va='bottom', fontsize=6.5, rotation=45)

        ax.set_xlabel('Arsitektur DL', fontsize=11)
        ax.set_ylabel('Score', fontsize=11)
        ax.set_title(
            f'Perbandingan 6 Variasi Arsitektur DL (threshold={THRESHOLD}, max {EPOCHS} epochs)',
            fontsize=12, fontweight='bold'
        )
        ax.set_xticks(x + width * 2)
        ax.set_xticklabels(names, rotation=12, ha='right', fontsize=9)
        ax.set_ylim(0, 1.08)
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.axhline(y=0.70, color='red', linestyle=':', alpha=0.5, label='Recall target 0.70')

        # Highlight baseline (index 0)
        ax.axvspan(x[0] - 0.1, x[0] + width * 5 + 0.1, alpha=0.05, color='green')

        plt.tight_layout()
        out = REPORTS_DIR / 'dl_experiments_comparison.png'
        plt.savefig(out, dpi=150, bbox_inches='tight')
        plt.close()
        log.info('Saved %s', out)
    except Exception as e:
        log.warning('Plot gagal: %s', e)


def main():
    import tensorflow as tf
    from imblearn.over_sampling import SMOTE
    from sklearn.preprocessing import StandardScaler
    from sklearn.utils.class_weight import compute_class_weight

    log.info('=== DL Architecture Experiments ===')
    log.info('Loading data...')
    X_train, X_test, y_train, y_test = load_data()

    with open(MODELS_DIR / 'feature_metadata.json') as f:
        feature_meta = json.load(f)
    feature_order = feature_meta['feature_order']
    X_train = X_train[feature_order]
    X_test = X_test[feature_order]

    log.info('Applying SMOTE...')
    smote = SMOTE(random_state=RANDOM_STATE, sampling_strategy=0.3)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train_res).astype('float32')
    X_test_s = scaler.transform(X_test).astype('float32')
    y_train_arr = np.asarray(y_train_res, dtype='float32')
    y_test_arr = np.asarray(y_test, dtype='float32')

    cw = compute_class_weight('balanced', classes=np.array([0, 1]), y=y_train_arr)
    class_weight = {0: float(cw[0]), 1: float(cw[1])}

    results = []
    for i, variant in enumerate(VARIANTS):
        log.info('--- [%d/%d] Training: %s ---', i + 1, len(VARIANTS), variant['name'])
        try:
            result = train_variant(
                variant, X_train_s, y_train_arr,
                X_test_s, y_test_arr, class_weight
            )
            results.append(result)
            log.info(
                '  acc=%.4f | recall=%.4f | precision=%.4f | f1=%.4f | auc=%.4f | %.1fs',
                result['accuracy'], result['recall'], result['precision'],
                result['f1'], result['roc_auc'], result['train_seconds']
            )
        except Exception as e:
            log.error('Variant %s gagal: %s', variant['name'], e)
            results.append({'name': variant['name'], 'error': str(e)})

    out_json = REPORTS_DIR / 'dl_experiments.json'
    with open(out_json, 'w') as f:
        json.dump(results, f, indent=2)
    log.info('Saved %s', out_json)

    # Print summary table
    log.info('\n=== RESULTS SUMMARY ===')
    log.info('%-25s %8s %8s %8s %8s %8s', 'Variant', 'Acc', 'Recall', 'Precision', 'F1', 'AUC')
    for r in results:
        if 'error' not in r:
            log.info('%-25s %8.4f %8.4f %8.4f %8.4f %8.4f',
                     r['name'][:25], r['accuracy'], r['recall'],
                     r['precision'], r['f1'], r['roc_auc'])

    valid_results = [r for r in results if 'error' not in r]
    if valid_results:
        plot_comparison(valid_results)

    log.info('Done.')
    return results


if __name__ == '__main__':
    main()
