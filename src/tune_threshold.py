from typing import Dict, Tuple

import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score


def find_best_threshold(model, X_valid, y_valid) -> Tuple[float, float]:
    """
    Find the threshold that maximizes F1-score.

    Parameters
    ----------
    model : fitted estimator
    X_valid : array-like
    y_valid : array-like

    Returns
    -------
    Tuple[float, float]
        Best threshold and corresponding F1-score.
    """
    y_proba = model.predict_proba(X_valid)[:, 1]
    thresholds = np.arange(0.10, 0.91, 0.05)

    best_threshold = 0.50
    best_f1 = -1.0

    for threshold in thresholds:
        y_pred = (y_proba >= threshold).astype(int)
        current_f1 = f1_score(y_valid, y_pred, zero_division=0)

        if current_f1 > best_f1:
            best_f1 = current_f1
            best_threshold = float(threshold)

    return best_threshold, float(best_f1)


def evaluate_thresholds(model, X_valid, y_valid) -> Dict[float, Dict[str, float]]:
    """
    Evaluate multiple thresholds for comparison.

    Returns
    -------
    dict
    """
    y_proba = model.predict_proba(X_valid)[:, 1]
    thresholds = np.arange(0.10, 0.91, 0.05)

    results = {}

    for threshold in thresholds:
        y_pred = (y_proba >= threshold).astype(int)
        results[float(threshold)] = {
            "precision": float(precision_score(y_valid, y_pred, zero_division=0)),
            "recall": float(recall_score(y_valid, y_pred, zero_division=0)),
            "f1": float(f1_score(y_valid, y_pred, zero_division=0)),
        }

    return results
