"""
doEVC.analysis.plots – Visualisation helpers for DoE analysis.
"""

from __future__ import annotations

from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main_effects_plot(
    data: pd.DataFrame,
    factors: List[str],
    response: str,
    ax: Optional[plt.Axes] = None,
) -> plt.Figure:
    """Plot the main effect of each factor on the response.

    Parameters
    ----------
    data:
        DataFrame with factor columns and a response column.
    factors:
        List of factor column names.
    response:
        Name of the response column.
    ax:
        Optional Axes to draw into; a new figure is created when ``None``.

    Returns
    -------
    matplotlib.figure.Figure
    """
    n = len(factors)
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 4), sharey=True)
    if n == 1:
        axes = [axes]
    for ax_i, factor in zip(axes, factors):
        means = data.groupby(factor)[response].mean()
        ax_i.plot(means.index, means.values, marker="o", linewidth=2)
        ax_i.set_xlabel(factor)
        ax_i.set_ylabel(response if factor == factors[0] else "")
        ax_i.set_title(f"Main effect: {factor}")
        ax_i.grid(True, linestyle="--", alpha=0.5)
    fig.suptitle("Main Effects Plot", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig


def interaction_plot(
    data: pd.DataFrame,
    factor1: str,
    factor2: str,
    response: str,
) -> plt.Figure:
    """Plot the interaction between two factors on the response.

    Parameters
    ----------
    data:
        DataFrame with factor columns and a response column.
    factor1:
        Name of the first factor (plotted on the x-axis).
    factor2:
        Name of the second factor (line colours / styles).
    response:
        Name of the response column.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    for level, group in data.groupby(factor2):
        means = group.groupby(factor1)[response].mean()
        ax.plot(means.index, means.values, marker="o", label=f"{factor2}={level}", linewidth=2)
    ax.set_xlabel(factor1)
    ax.set_ylabel(response)
    ax.set_title(f"Interaction Plot: {factor1} × {factor2}")
    ax.legend(title=factor2)
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    return fig
