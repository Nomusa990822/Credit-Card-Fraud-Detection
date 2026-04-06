from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split


def split_train_valid(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Split the dataset into train and validation sets using stratification.

    Parameters
    ----------
    X : pd.DataFrame
    y : pd.Series
    test_size : float
    random_state : int

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]
    """
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )
