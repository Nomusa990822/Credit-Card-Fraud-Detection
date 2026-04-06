from pathlib import Path
from typing import Optional, Tuple

import pandas as pd


def load_csv(path: str) -> pd.DataFrame:
    """
    Load a CSV file from disk.

    Parameters
    ----------
    path : str
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded dataframe.
    """
    csv_path = Path(path)

    if not csv_path.exists():
        raise FileNotFoundError(f"File not found: {csv_path}")

    return pd.read_csv(csv_path)


def load_data(
    train_path: str = "data/raw/train.csv",
    test_path: Optional[str] = "data/raw/test.csv"
) -> Tuple[pd.DataFrame, Optional[pd.DataFrame]]:
    """
    Load train and optional test datasets.

    Parameters
    ----------
    train_path : str
        Path to the training CSV file.
    test_path : Optional[str]
        Path to the test CSV file. If missing, returns None for test_df.

    Returns
    -------
    Tuple[pd.DataFrame, Optional[pd.DataFrame]]
        Training dataframe and optional test dataframe.
    """
    train_df = load_csv(train_path)

    test_df = None
    if test_path is not None and Path(test_path).exists():
        test_df = load_csv(test_path)

    return train_df, test_df
