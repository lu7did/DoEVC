"""
doEVC.design.response_surface – Central Composite Design (CCD) helper.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pyDOE3


def central_composite(
    n_factors: int,
    alpha: str = "orthogonal",
    face: str = "ccc",
    center: tuple[int, int] = (4, 4),
) -> pd.DataFrame:
    """Build a Central Composite Design (CCD) for Response Surface Methodology.

    Parameters
    ----------
    n_factors:
        Number of continuous factors.
    alpha:
        Star-point placement: ``"orthogonal"``, ``"rotatable"``, or a
        float specifying the axial distance directly.
    face:
        CCD face type: ``"ccc"`` (circumscribed), ``"cci"`` (inscribed),
        or ``"ccf"`` (face-centred).
    center:
        ``(n_center_factorial, n_center_star)`` – number of centre points
        in the factorial and star portions.

    Returns
    -------
    pd.DataFrame
        Coded design matrix. Columns labelled ``x1, x2, …``.

    Examples
    --------
    >>> ccd = central_composite(2)
    >>> ccd.shape[1]
    2
    """
    matrix = pyDOE3.ccdesign(n_factors, center=center, alpha=alpha, face=face)
    columns = [f"x{i + 1}" for i in range(matrix.shape[1])]
    return pd.DataFrame(matrix, columns=columns)
