from typing import Dict, Tuple

import pandas as pd

from src.data_ingestion import load_data
from src.evaluate import evaluate_model, summarize_model_performance
from src.feature_engineering import engineer_features
from src.preprocessing import (
    add_log_amount_feature,
    basic_cleaning,
    ensure_numeric_columns,
    fill_missing_values,
    fit_scaler,
    split_features_target,
    transform_with_scaler,
)
from src.save_artifacts import (
    save_feature_columns,
    save_metrics,
    save_model,
    save_scaler,
    save_threshold,
)
from src.split_data import split_train_valid
from src.train import train_all_models
from src.tune_threshold import find_best_threshold


def preprocess_training_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all preprocessing and feature engineering steps needed for training.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    processed = df.copy()
    processed = basic_cleaning(processed)
    processed = ensure_numeric_columns(processed, exclude_cols=[])
    processed = add_log_amount_feature(processed)
    processed = engineer_features(processed)
    processed = fill_missing_values(processed)
    return processed


def select_best_model(models: Dict[str, object], X_valid, y_valid) -> Tuple[str, object, Dict]:
    """
    Select the best model based on ROC-AUC at threshold 0.5.

    Parameters
    ----------
    models : dict[str, object]
    X_valid : array-like
    y_valid : array-like

    Returns
    -------
    Tuple[str, object, dict]
        Best model name, best model object, and evaluation metrics.
    """
    best_model_name = None
    best_model = None
    best_metrics = None
    best_score = -1.0

    for model_name, model in models.items():
        metrics = evaluate_model(model, X_valid, y_valid, threshold=0.5)
        print(summarize_model_performance(model_name, metrics))

        if metrics["roc_auc"] > best_score:
            best_score = metrics["roc_auc"]
            best_model_name = model_name
            best_model = model
            best_metrics = metrics

    return best_model_name, best_model, best_metrics


def run_training_pipeline() -> None:
    """
    End-to-end training pipeline:
    - load data
    - preprocess
    - engineer features
    - split data
    - scale features
    - train multiple models
    - select best model
    - tune threshold
    - save artifacts and metrics
    """
    print("Loading data...")
    train_df, _ = load_data()

    print("Preprocessing training data...")
    train_df = preprocess_training_dataframe(train_df)

    print("Splitting features and target...")
    X, y = split_features_target(train_df, target_col="isFraud")

    print("Creating train/validation split...")
    X_train, X_valid, y_train, y_valid = split_train_valid(X, y)

    print("Fitting scaler...")
    scaler = fit_scaler(X_train)
    X_train_scaled = transform_with_scaler(scaler, X_train)
    X_valid_scaled = transform_with_scaler(scaler, X_valid)

    print("Training models...")
    models = train_all_models(X_train_scaled, y_train)

    print("Selecting best model...")
    best_model_name, best_model, _ = select_best_model(models, X_valid_scaled, y_valid)
    print(f"Best model selected: {best_model_name}")

    print("Tuning threshold...")
    best_threshold, best_f1 = find_best_threshold(best_model, X_valid_scaled, y_valid)

    print("Evaluating best model at tuned threshold...")
    tuned_metrics = evaluate_model(best_model, X_valid_scaled, y_valid, threshold=best_threshold)

    final_metrics = {
        "best_model": best_model_name,
        "best_threshold": best_threshold,
        "best_f1_at_tuned_threshold": best_f1,
        **tuned_metrics
    }

    print("Saving artifacts...")
    save_model(best_model)
    save_scaler(scaler)
    save_feature_columns(list(X_train.columns))
    save_threshold(best_threshold)
    save_metrics(final_metrics)

    print("Training pipeline completed successfully.")
    print(f"Best model: {best_model_name}")
    print(f"Best threshold: {best_threshold:.2f}")
    print(f"Validation F1 at tuned threshold: {best_f1:.4f}")
