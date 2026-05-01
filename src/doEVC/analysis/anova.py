"""
doEVC.analysis.anova – ANOVA helpers for DoE response analysis.
"""

from __future__ import annotations

from typing import List

import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols


def one_way_anova(data: pd.DataFrame, factor: str, response: str) -> pd.DataFrame:
    """Perform a one-way ANOVA.

    Parameters
    ----------
    data:
        DataFrame containing the experimental data.
    factor:
        Name of the column with the grouping factor.
    response:
        Name of the column with the response variable.

    Returns
    -------
    pd.DataFrame
        ANOVA table (sum of squares, df, F-statistic, p-value).

    Examples
    --------
    >>> import pandas as pd
    >>> data = pd.DataFrame({"group": ["A","A","B","B"], "y": [1.0, 1.1, 2.0, 2.1]})
    >>> tbl = one_way_anova(data, "group", "y")
    >>> "PR(>F)" in tbl.columns
    True
    """
    model = ols(f"{response} ~ C({factor})", data=data).fit()
    anova_table = sm.stats.anova_lm(model, typ=1)
    return anova_table


def two_way_anova(
    data: pd.DataFrame,
    factors: List[str],
    response: str,
    interaction: bool = True,
) -> pd.DataFrame:
    """Perform a two-way ANOVA, optionally including the interaction term.

    Parameters
    ----------
    data:
        DataFrame containing the experimental data.
    factors:
        List of exactly two factor column names.
    response:
        Name of the response column.
    interaction:
        When ``True``, include the two-factor interaction term.

    Returns
    -------
    pd.DataFrame
        ANOVA table.

    Raises
    ------
    ValueError
        If *factors* does not contain exactly two names.
    """
    if len(factors) != 2:
        raise ValueError(f"two_way_anova requires exactly 2 factors; got {len(factors)}.")
    f1, f2 = factors
    formula = f"{response} ~ C({f1}) + C({f2})"
    if interaction:
        formula += f" + C({f1}):C({f2})"
    model = ols(formula, data=data).fit()
    return sm.stats.anova_lm(model, typ=2)
