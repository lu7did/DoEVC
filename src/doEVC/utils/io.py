"""
doEVC.utils.io – Data I/O helpers.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_csv(path: str | Path, **kwargs) -> pd.DataFrame:
    """Load experimental data from a CSV file.

    Parameters
    ----------
    path:
        Path to the CSV file.
    **kwargs:
        Additional keyword arguments forwarded to :func:`pandas.read_csv`.

    Returns
    -------
    pd.DataFrame
    """
    return pd.read_csv(Path(path), **kwargs)


def save_csv(data: pd.DataFrame, path: str | Path, index: bool = False, **kwargs) -> None:
    """Save a DataFrame to a CSV file.

    Parameters
    ----------
    data:
        DataFrame to save.
    path:
        Destination path.
    index:
        Whether to include the row index in the output file.
    **kwargs:
        Additional keyword arguments forwarded to :func:`pandas.DataFrame.to_csv`.
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(Path(path), index=index, **kwargs)
