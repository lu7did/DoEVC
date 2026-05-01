"""
doEVC.analysis.response_surface – Response Surface Model fitting.
"""

from __future__ import annotations

import pandas as pd
import numpy as np
import statsmodels.api as sm


def fit_response_surface(
    design: pd.DataFrame,
    response: pd.Series | np.ndarray,
    order: int = 2,
) -> sm.regression.linear_model.RegressionResultsWrapper:
    """Fit a polynomial response surface model.

    Parameters
    ----------
    design:
        Coded factor matrix (rows = runs, columns = factors x1, x2, …).
    response:
        Observed response values, one per run.
    order:
        Polynomial order: 1 (linear) or 2 (quadratic with cross-terms).

    Returns
    -------
    statsmodels RegressionResults
        Fitted OLS model.  Call ``.summary()`` for a full report.

    Raises
    ------
    ValueError
        If *order* is not 1 or 2.
    """
    if order not in (1, 2):
        raise ValueError(f"order must be 1 or 2; got {order}.")

    X = design.copy()

    if order == 2:
        cols = list(design.columns)
        # Add squared terms
        for col in cols:
            X[f"{col}²"] = design[col] ** 2
        # Add cross-product terms
        for i, ci in enumerate(cols):
            for cj in cols[i + 1 :]:
                X[f"{ci}×{cj}"] = design[ci] * design[cj]

    X = sm.add_constant(X)
    model = sm.OLS(response, X).fit()
    return model
