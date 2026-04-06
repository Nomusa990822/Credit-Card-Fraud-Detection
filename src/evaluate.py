from typing import Dict, List

import numpy as np
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score
)


def evaluate_model(model, X_valid, y_valid, threshold: float = 0.5) -> Dict:
    """
    Evaluate a trained model at a given threshold.

    Parameters
    ----------
    model : fitted estimator
    X_valid : array-like
    y_valid : array-like
    threshold : float

    Returns
    -------
    dict
    """
    y_proba = model.predict_proba(X_valid)[:, 1]
    y_pred = (y_proba >= threshold).astype(int)

    metrics = {
        "roc_auc": float(roc_auc_score(y_valid, y_proba)),
        "pr_auc": float(average_precision_score(y_valid, y_proba)),
        "precision": float(precision_score(y_valid, y_pred, zero_division=0)),
        "recall": float(recall_score(y_valid, y_pred, zero_division=0)),
        "f1": float(f1_score(y_valid, y_pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_valid, y_pred).tolist(),
        "classification_report": classification_report(y_valid, y_pred, zero_division=0)
    }

    return metrics


def summarize_model_performance(model_name: str, metrics: Dict) -> str:
    """
    Create a short summary string for model performance.

    Parameters
    ----------
    model_name : str
    metrics : dict

    Returns
    -------
    str
    """
    return (
        f"{model_name}: "
        f"ROC-AUC={metrics['roc_auc']:.4f}, "
        f"PR-AUC={metrics['pr_auc']:.4f}, "
        f"Precision={metrics['precision']:.4f}, "
        f"Recall={metrics['recall']:.4f}, "
        f"F1={metrics['f1']:.4f}"
    )
