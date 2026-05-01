"""
doEVC.utils.reproducibility – Seed management for reproducible experiments.
"""

from __future__ import annotations

import random

import numpy as np


def set_seed(seed: int) -> None:
    """Set the random seed for NumPy and Python's built-in ``random`` module.

    Call this at the top of a notebook or script to ensure reproducible
    experimental designs and analysis results.

    Parameters
    ----------
    seed:
        Integer seed value.

    Examples
    --------
    >>> set_seed(42)
    """
    np.random.seed(seed)
    random.seed(seed)
