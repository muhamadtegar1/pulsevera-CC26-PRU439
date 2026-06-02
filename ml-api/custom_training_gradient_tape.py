"""
Custom Training Loop dengan tf.GradientTape — Pulsevera AI Side Quest (P2-4)

Implementasi manual training loop menggunakan tf.GradientTape sebagai alternatif
dari model.fit(). Arsitektur identik dengan baseline DL (Dense[256-128-64-1]).

Jalankan:
    cd ml-api
    python custom_training_gradient_tape.py

Output:
    reports/gradient_tape_training_history.json  — loss/metric per epoch
    reports/gradient_tape_results.json           — final test metrics
"""
from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf
import keras
from keras import layers

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger('gradient-tape')

BASE_DIR = Path(__file__).resolve().parent.parent
FINAL_DIR = BASE_DIR / 'data' / 'final'
MODELS_DIR = Path(__file__).parent / 'models'
REPORTS_DIR = BASE_DIR / 'reports'
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
EPOCHS = 20
BATCH_SIZE = 512
THRESHOLD = 0.23


def load_data():
    X_train = pd.read_csv(FINAL_DIR / 'X_train.csv')
    X_test = pd.read_csv(FINAL_DIR / 'X_test.csv')
    y_train = pd.read_csv(FINAL_DIR / 'y_train.csv').squeeze()
    y_test = pd.read_csv(FINAL_DIR / 'y_test.csv').squeeze()
    bool_cols = X_train.select_dtypes(include='bool').columns
    X_train[bool_cols] = X_train[bool_cols].astype('float32')
    X_test[bool_cols] = X_test[bool_cols].astype('float32')
    log.info('Data loaded — X_train=%s, X_test=%s', X_train.shape, X_test.shape)
    return X_train, X_test, y_train, y_test


def build_model(n_features: int) -> keras.Model:
    inp = keras.Input(shape=(n_features,), name='lifestyle_input')
    x = layers.Dense(256, activation='relu', kernel_initializer='he_normal')(inp)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(128, activation='relu', kernel_initializer='he_normal')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(64, activation='relu', kernel_initializer='he_normal')(x)
    x = layers.Dropout(0.15)(x)
    out = layers.Dense(1, activation='sigmoid', name='heart_attack_risk')(x)
    return keras.Model(inputs=inp, outputs=out, name='pulsevera_gradient_tape')


@tf.function
def train_step(model, optimizer, X_batch, y_batch, cw0, cw1):
    """Single training step using tf.GradientTape."""
    with tf.GradientTape() as tape:
        y_pred = tf.squeeze(model(X_batch, training=True))
        y_true = tf.cast(y_batch, tf.float32)

        # Per-sample Focal Loss: FL(p_t) = -alpha_t * (1-p_t)^gamma * log(p_t)
        y_pred_clip = tf.clip_by_value(y_pred, 1e-7, 1.0 - 1e-7)
        bce = -(y_true * tf.math.log(y_pred_clip)
                + (1.0 - y_true) * tf.math.log(1.0 - y_pred_clip))
        p_t = y_true * y_pred_clip + (1.0 - y_true) * (1.0 - y_pred_clip)
        alpha_t = y_true * 0.25 + (1.0 - y_true) * 0.75
        per_sample_loss = alpha_t * tf.pow(1.0 - p_t, 2.0) * bce

        # Class weights untuk menangani imbalance
        sample_weights = y_true * cw1 + (1.0 - y_true) * cw0
        loss = tf.reduce_mean(per_sample_loss * sample_weights)

    grads = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(grads, model.trainable_variables))
    return loss


def eval_batch(model, X_batch, y_batch, threshold: float = THRESHOLD):
    """Evaluate one batch — returns (correct, tp, fp, fn, n)."""
    y_pred = tf.squeeze(model(X_batch, training=False)).numpy()
    y_pred_bin = (y_pred >= threshold).astype('float32')
    y_true = y_batch.astype('float32')
    correct = float(np.sum(y_pred_bin == y_true))
    tp = float(np.sum(y_pred_bin * y_true))
    fp = float(np.sum(y_pred_bin * (1.0 - y_true)))
    fn = float(np.sum((1.0 - y_pred_bin) * y_true))
    return correct, tp, fp, fn, len(y_true)


def main():
    from imblearn.over_sampling import SMOTE
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import (
        accuracy_score, f1_score, precision_score, recall_score, roc_auc_score,
    )
    from sklearn.utils.class_weight import compute_class_weight

    tf.random.set_seed(RANDOM_STATE)
    np.random.seed(RANDOM_STATE)

    log.info('Loading data...')
    X_train, X_test, y_train, y_test = load_data()

    with open(MODELS_DIR / 'feature_metadata.json') as f:
        feature_meta = json.load(f)
    feature_order = feature_meta['feature_order']
    X_train = X_train[feature_order]
    X_test = X_test[feature_order]

    log.info('Applying SMOTE (sampling_strategy=0.3)...')
    smote = SMOTE(random_state=RANDOM_STATE, sampling_strategy=0.3)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    log.info('After SMOTE: %s | positif=%d', X_train_res.shape, int((y_train_res == 1).sum()))

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train_res).astype('float32')
    X_test_s = scaler.transform(X_test).astype('float32')
    y_train_arr = np.asarray(y_train_res, dtype='float32')
    y_test_arr = np.asarray(y_test, dtype='float32')

    cw = compute_class_weight('balanced', classes=np.array([0, 1]), y=y_train_arr)
    cw0, cw1 = tf.constant(float(cw[0])), tf.constant(float(cw[1]))
    log.info('Class weights: 0=%.3f, 1=%.3f', float(cw[0]), float(cw[1]))

    # 80/20 train-val split (match model.fit behaviour)
    split = int(len(X_train_s) * 0.8)
    X_tr, X_val = X_train_s[:split], X_train_s[split:]
    y_tr, y_val = y_train_arr[:split], y_train_arr[split:]

    train_ds = (tf.data.Dataset.from_tensor_slices((X_tr, y_tr))
                .shuffle(10000, seed=RANDOM_STATE)
                .batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE))
    val_ds = (tf.data.Dataset.from_tensor_slices((X_val, y_val))
              .batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE))

    log.info('Building model...')
    model = build_model(X_train_s.shape[1])
    optimizer = keras.optimizers.Adam(learning_rate=1e-3)

    history = {'train_loss': [], 'val_accuracy': [], 'val_recall': [], 'val_precision': []}
    best_recall, best_weights, patience, wait = 0.0, None, 5, 0
    last_epoch = 0

    log.info('Starting custom training loop — %d epochs, batch_size=%d', EPOCHS, BATCH_SIZE)
    t_start = time.time()

    for epoch in range(1, EPOCHS + 1):
        last_epoch = epoch
        batch_losses = [float(train_step(model, optimizer, Xb, yb, cw0, cw1))
                        for Xb, yb in train_ds]
        mean_loss = float(np.mean(batch_losses))

        tot_c, tot_tp, tot_fp, tot_fn, tot_n = 0.0, 0.0, 0.0, 0.0, 0
        for Xb, yb in val_ds:
            c, tp, fp, fn, n = eval_batch(model, Xb.numpy(), yb.numpy())
            tot_c += c; tot_tp += tp; tot_fp += fp; tot_fn += fn; tot_n += n

        val_acc = tot_c / tot_n if tot_n else 0.0
        val_rec = tot_tp / (tot_tp + tot_fn) if (tot_tp + tot_fn) else 0.0
        val_pre = tot_tp / (tot_tp + tot_fp) if (tot_tp + tot_fp) else 0.0

        history['train_loss'].append(mean_loss)
        history['val_accuracy'].append(val_acc)
        history['val_recall'].append(val_rec)
        history['val_precision'].append(val_pre)

        log.info(
            'Epoch %02d/%02d — loss=%.4f | val_acc=%.4f | val_recall=%.4f | val_precision=%.4f',
            epoch, EPOCHS, mean_loss, val_acc, val_rec, val_pre,
        )

        if val_rec - best_recall > 1e-3:
            best_recall, best_weights, wait = val_rec, model.get_weights(), 0
        else:
            wait += 1
            if wait >= patience:
                log.info('Early stopping at epoch %d (best recall=%.4f)', epoch, best_recall)
                break

    if best_weights:
        model.set_weights(best_weights)

    elapsed = time.time() - t_start
    log.info('Training complete in %.1f seconds', elapsed)

    y_proba = model.predict(X_test_s, batch_size=1024, verbose=0).ravel()
    y_pred = (y_proba >= THRESHOLD).astype(int)

    results = {
        'method': 'tf.GradientTape custom loop',
        'architecture': 'Dense[256-128-64-1] + BN + Dropout',
        'epochs_trained': last_epoch,
        'threshold': THRESHOLD,
        'train_time_seconds': round(elapsed, 1),
        'test_accuracy': float(accuracy_score(y_test_arr, y_pred)),
        'test_recall': float(recall_score(y_test_arr, y_pred, pos_label=1, zero_division=0)),
        'test_precision': float(precision_score(y_test_arr, y_pred, pos_label=1, zero_division=0)),
        'test_f1': float(f1_score(y_test_arr, y_pred, pos_label=1, zero_division=0)),
        'test_roc_auc': float(roc_auc_score(y_test_arr, y_proba)),
    }

    log.info(
        'Test — acc=%.4f | recall=%.4f | precision=%.4f | f1=%.4f | auc=%.4f',
        results['test_accuracy'], results['test_recall'],
        results['test_precision'], results['test_f1'], results['test_roc_auc'],
    )

    with open(REPORTS_DIR / 'gradient_tape_training_history.json', 'w') as f:
        json.dump(history, f, indent=2)
    with open(REPORTS_DIR / 'gradient_tape_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    log.info('Saved reports/gradient_tape_*.json')
    log.info('Done.')
    return results


if __name__ == '__main__':
    main()
