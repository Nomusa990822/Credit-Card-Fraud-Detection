import json
from pathlib import Path
from typing import List

import joblib


ARTIFACT_DIR = Path("artifacts")


def ensure_artifact_dir() -> None:
    """
    Ensure the artifact directory exists.
    """
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def save_model(model, filename: str = "model.pkl") -> None:
    """
    Save trained model to disk.
    """
    ensure_artifact_dir()
    joblib.dump(model, ARTIFACT_DIR / filename)


def save_scaler(scaler, filename: str = "scaler.pkl") -> None:
    """
    Save scaler to disk.
    """
    ensure_artifact_dir()
    joblib.dump(scaler, ARTIFACT_DIR / filename)


def save_feature_columns(columns: List[str], filename: str = "feature_columns.pkl") -> None:
    """
    Save feature column names to disk.
    """
    ensure_artifact_dir()
    joblib.dump(columns, ARTIFACT_DIR / filename)


def save_threshold(threshold: float, filename: str = "threshold.json") -> None:
    """
    Save selected decision threshold to disk.
    """
    ensure_artifact_dir()
    with open(ARTIFACT_DIR / filename, "w", encoding="utf-8") as file:
        json.dump({"threshold": threshold}, file, indent=2)


def save_metrics(metrics: dict, filename: str = "tuned_metrics.json") -> None:
    """
    Save evaluation metrics to reports/metrics.
    """
    metrics_dir = Path("reports/metrics")
    metrics_dir.mkdir(parents=True, exist_ok=True)

    with open(metrics_dir / filename, "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)
