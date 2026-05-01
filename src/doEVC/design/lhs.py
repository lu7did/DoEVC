"""
doEVC.design.lhs – Latin Hypercube Sampling (LHS) helper.
"""

from __future__ import annotations

import pandas as pd
import pyDOE3


def latin_hypercube(
    n_factors: int,
    n_samples: int,
    criterion: str | None = "maximin",
    seed: int | None = None,
) -> pd.DataFrame:
    """Generate a Latin Hypercube Sample in the unit hypercube [0, 1]^k.

    Parameters
    ----------
    n_factors:
        Number of factors (dimensions).
    n_samples:
        Number of sample points.
    criterion:
        Optimality criterion for pyDOE3: ``"center"``, ``"maximin"``,
        ``"centermaximin"``, ``"correlation"``, or ``None`` for a random LHS.
    seed:
        Integer random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        Sample matrix of shape ``(n_samples, n_factors)``.
        Columns labelled ``x1, x2, …``.

    Examples
    --------
    >>> lhs = latin_hypercube(3, 10, seed=42)
    >>> lhs.shape
    (10, 3)
    """
    matrix = pyDOE3.lhs(n_factors, samples=n_samples, criterion=criterion, seed=seed)
    columns = [f"x{i + 1}" for i in range(n_factors)]
    return pd.DataFrame(matrix, columns=columns)
