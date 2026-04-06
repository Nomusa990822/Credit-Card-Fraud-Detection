from typing import Dict, Tuple

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier


def compute_scale_pos_weight(y_train) -> float:
    """
    Compute scale_pos_weight for imbalanced classification.

    Parameters
    ----------
    y_train : array-like

    Returns
    -------
    float
    """
    y_array = np.asarray(y_train)
    positive_count = (y_array == 1).sum()
    negative_count = (y_array == 0).sum()

    if positive_count == 0:
        return 1.0

    return float(negative_count / positive_count)


def train_logistic_regression(X_train, y_train) -> LogisticRegression:
    """
    Train a Logistic Regression model.

    Returns
    -------
    LogisticRegression
    """
    model = LogisticRegression(
        class_weight="balanced",
        max_iter=2000,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model


def train_random_forest(X_train, y_train) -> RandomForestClassifier:
    """
    Train a Random Forest model.

    Returns
    -------
    RandomForestClassifier
    """
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model


def train_xgboost(X_train, y_train) -> XGBClassifier:
    """
    Train an XGBoost classifier.

    Returns
    -------
    XGBClassifier
    """
    scale_pos_weight = compute_scale_pos_weight(y_train)

    model = XGBClassifier(
        n_estimators=400,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        reg_alpha=0.0,
        reg_lambda=1.0,
        scale_pos_weight=scale_pos_weight,
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model


def train_all_models(X_train, y_train) -> Dict[str, object]:
    """
    Train multiple models and return them in a dictionary.

    Returns
    -------
    dict[str, object]
    """
    models = {
        "logistic_regression": train_logistic_regression(X_train, y_train),
        "random_forest": train_random_forest(X_train, y_train),
        "xgboost": train_xgboost(X_train, y_train),
    }
    return models
