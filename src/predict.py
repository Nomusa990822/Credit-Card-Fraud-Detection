import json
from pathlib import Path
from typing import Dict, List

import joblib
import pandas as pd

from src.feature_engineering import engineer_features
from src.preprocessing import add_log_amount_feature, basic_cleaning, fill_missing_values


ARTIFACT_DIR = Path("artifacts")


def load_model():
    """
    Load trained model from disk.
    """
    return joblib.load(ARTIFACT_DIR / "model.pkl")


def load_scaler():
    """
    Load fitted scaler from disk.
    """
    return joblib.load(ARTIFACT_DIR / "scaler.pkl")


def load_feature_columns() -> List[str]:
    """
    Load expected feature columns from disk.
    """
    return joblib.load(ARTIFACT_DIR / "feature_columns.pkl")


def load_threshold() -> float:
    """
    Load decision threshold from disk.
    """
    with open(ARTIFACT_DIR / "threshold.json", "r", encoding="utf-8") as file:
        return float(json.load(file)["threshold"])


def align_features(df: pd.DataFrame, feature_columns: List[str]) -> pd.DataFrame:
    """
    Align a dataframe to the exact expected feature columns.

    Missing columns are added with zeros.
    Extra columns are removed.

    Parameters
    ----------
    df : pd.DataFrame
    feature_columns : list[str]

    Returns
    -------
    pd.DataFrame
    """
    aligned = df.copy()

    for col in feature_columns:
        if col not in aligned.columns:
            aligned[col] = 0

    aligned = aligned[feature_columns]
    return aligned


def prepare_inference_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the same preprocessing and feature engineering used in training.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    prepared = df.copy()
    prepared = basic_cleaning(prepared)
    prepared = add_log_amount_feature(prepared)
    prepared = engineer_features(prepared)
    prepared = fill_missing_values(prepared)
    return prepared


def predict_single(record: Dict) -> Dict:
    """
    Predict fraud probability for a single transaction record.

    Parameters
    ----------
    record : dict

    Returns
    -------
    dict
    """
    model = load_model()
    scaler = load_scaler()
    feature_columns = load_feature_columns()
    threshold = load_threshold()

    df = pd.DataFrame([record])
    df = prepare_inference_dataframe(df)
    df = align_features(df, feature_columns)

    X = scaler.transform(df)
    probability = float(model.predict_proba(X)[:, 1][0])
    predicted_class = int(probability >= threshold)

    if probability < 0.30:
        risk_level = "low"
    elif probability < 0.70:
        risk_level = "medium"
    else:
        risk_level = "high"

    return {
        "fraud_probability": round(probability, 6),
        "predicted_class": predicted_class,
        "risk_level": risk_level
    }


def predict_batch(records: List[Dict]) -> List[Dict]:
    """
    Predict fraud probabilities for multiple transaction records.

    Parameters
    ----------
    records : list[dict]

    Returns
    -------
    list[dict]
    """
    return [predict_single(record) for record in records]
