"""
doEVC.design.factorial – Full and fractional factorial design helpers.
"""

from __future__ import annotations

from itertools import product
from typing import Dict, List, Sequence

import numpy as np
import pandas as pd
import pyDOE3

# Minimum-aberration generator strings for 2^(k-p) designs up to k=7.
# Each entry maps the number of factors to a pyDOE3 fracfact generator string
# that produces a resolution-≥IV design whenever possible.
_FRACFACT_GENERATORS: dict[int, str] = {
    3: "a b c",           # 2^3 full factorial (8 runs) – smallest meaningful case
    4: "a b c abc",       # 2^(4-1) resolution IV  (8 runs)
    5: "a b c d abcd",    # 2^(5-1) resolution V  (16 runs)
    6: "a b c d e abcde", # 2^(6-1) resolution VI (32 runs)
    7: "a b c d e f abcdef",  # 2^(7-1) resolution VII (64 runs)
}


def full_factorial(factors: Dict[str, Sequence]) -> pd.DataFrame:
    """Build a full factorial design from a mapping of factor names to levels.

    Parameters
    ----------
    factors:
        Ordered mapping ``{factor_name: [level_0, level_1, ...]}``.

    Returns
    -------
    pd.DataFrame
        Each row is one experimental run; columns are the factor names.

    Examples
    --------
    >>> design = full_factorial({"V_ref": [4.8, 5.0, 5.2], "load": [10, 50]})
    >>> len(design)  # 3 × 2 = 6 runs
    6
    """
    names = list(factors.keys())
    levels = list(factors.values())
    runs = list(product(*levels))
    return pd.DataFrame(runs, columns=names)


def fractional_factorial(
    n_factors: int,
    generator: str | None = None,
) -> pd.DataFrame:
    """Build a two-level fractional factorial design using pyDOE3.

    When *generator* is ``None`` a minimum-aberration generator is chosen
    automatically for *n_factors* in the range 3–7.

    Parameters
    ----------
    n_factors:
        Number of factors (each at two coded levels: −1 and +1).
    generator:
        Optional pyDOE3 ``fracfact`` generator string (e.g. ``"a b c abc"``).
        When provided it is passed directly to :func:`pyDOE3.fracfact`.

    Returns
    -------
    pd.DataFrame
        Coded (−1 / +1) design matrix.  Columns labelled ``x1, x2, …``.

    Raises
    ------
    ValueError
        If *generator* is ``None`` and *n_factors* is not in 3–7.

    Examples
    --------
    >>> df = fractional_factorial(4)
    >>> df.shape  # 2^(4-1) = 8 runs, 4 columns
    (8, 4)
    """
    if generator is None:
        if n_factors not in _FRACFACT_GENERATORS:
            raise ValueError(
                f"No built-in generator for n_factors={n_factors}. "
                "Provide an explicit generator string."
            )
        generator = _FRACFACT_GENERATORS[n_factors]

    matrix = pyDOE3.fracfact(generator)
    columns = [f"x{i + 1}" for i in range(matrix.shape[1])]
    return pd.DataFrame(matrix, columns=columns)
