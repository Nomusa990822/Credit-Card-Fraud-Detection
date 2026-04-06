from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic dataframe cleaning:
    - copy input
    - remove duplicate rows
    - standardize column names by stripping whitespace

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    cleaned = df.copy()
    cleaned.columns = [col.strip() for col in cleaned.columns]
    cleaned = cleaned.drop_duplicates()
    return cleaned


def add_log_amount_feature(df: pd.DataFrame, amount_col: str = "Amount") -> pd.DataFrame:
    """
    Add a log-transformed amount feature.

    Parameters
    ----------
    df : pd.DataFrame
    amount_col : str

    Returns
    -------
    pd.DataFrame
    """
    transformed = df.copy()

    if amount_col in transformed.columns:
        transformed["Amount_log"] = np.log1p(transformed[amount_col].clip(lower=0))

    return transformed


def ensure_numeric_columns(df: pd.DataFrame, exclude_cols: List[str] | None = None) -> pd.DataFrame:
    """
    Convert columns to numeric where possible, excluding specified columns.

    Parameters
    ----------
    df : pd.DataFrame
    exclude_cols : list[str] | None

    Returns
    -------
    pd.DataFrame
    """
    exclude_cols = exclude_cols or []
    converted = df.copy()

    for col in converted.columns:
        if col not in exclude_cols:
            converted[col] = pd.to_numeric(converted[col], errors="coerce")

    return converted


def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing numeric values with column medians.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    filled = df.copy()
    numeric_cols = filled.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        filled[col] = filled[col].fillna(filled[col].median())

    return filled


def split_features_target(
    df: pd.DataFrame,
    target_col: str = "Class"
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Split dataframe into features and target.

    Parameters
    ----------
    df : pd.DataFrame
    target_col : str

    Returns
    -------
    Tuple[pd.DataFrame, pd.Series]
    """
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataframe.")

    X = df.drop(columns=[target_col]).copy()
    y = df[target_col].copy()

    return X, y


def fit_scaler(X_train: pd.DataFrame) -> StandardScaler:
    """
    Fit a StandardScaler on training data.

    Parameters
    ----------
    X_train : pd.DataFrame

    Returns
    -------
    StandardScaler
    """
    scaler = StandardScaler()
    scaler.fit(X_train)
    return scaler


def transform_with_scaler(scaler: StandardScaler, X: pd.DataFrame) -> np.ndarray:
    """
    Transform feature matrix using a fitted scaler.

    Parameters
    ----------
    scaler : StandardScaler
    X : pd.DataFrame

    Returns
    -------
    np.ndarray
    """
    return scaler.transform(X)
