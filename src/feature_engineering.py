import numpy as np
import pandas as pd


def create_time_features(df: pd.DataFrame, time_col: str = "Time") -> pd.DataFrame:
    """
    Create time-based features from the transaction time column.

    Parameters
    ----------
    df : pd.DataFrame
    time_col : str

    Returns
    -------
    pd.DataFrame
    """
    engineered = df.copy()

    if time_col in engineered.columns:
        engineered["hour_proxy"] = ((engineered[time_col] // 3600) % 24).astype(int)
        engineered["is_night"] = engineered["hour_proxy"].isin([0, 1, 2, 3, 4, 5]).astype(int)
        engineered["is_business_hours"] = engineered["hour_proxy"].between(8, 17).astype(int)

    return engineered


def create_amount_features(df: pd.DataFrame, amount_col: str = "Amount") -> pd.DataFrame:
    """
    Create amount-based features.

    Parameters
    ----------
    df : pd.DataFrame
    amount_col : str

    Returns
    -------
    pd.DataFrame
    """
    engineered = df.copy()

    if amount_col in engineered.columns:
        median_amount = engineered[amount_col].median()
        mean_amount = engineered[amount_col].mean()
        std_amount = engineered[amount_col].std()

        engineered["high_amount_flag"] = (engineered[amount_col] > median_amount).astype(int)
        engineered["amount_to_mean_ratio"] = engineered[amount_col] / (mean_amount + 1e-8)
        engineered["amount_zscore_like"] = (
            (engineered[amount_col] - mean_amount) / (std_amount + 1e-8)
        )
        engineered["amount_squared"] = engineered[amount_col] ** 2

    return engineered


def create_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a few lightweight interaction features.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    engineered = df.copy()

    if "Amount_log" in engineered.columns and "hour_proxy" in engineered.columns:
        engineered["amount_log_x_hour"] = engineered["Amount_log"] * engineered["hour_proxy"]

    if "Amount" in engineered.columns and "is_night" in engineered.columns:
        engineered["night_amount_interaction"] = engineered["Amount"] * engineered["is_night"]

    return engineered


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all feature engineering steps.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    engineered = df.copy()
    engineered = create_time_features(engineered)
    engineered = create_amount_features(engineered)
    engineered = create_interaction_features(engineered)
    return engineered
