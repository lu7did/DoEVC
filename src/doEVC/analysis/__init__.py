"""
doEVC.analysis – Statistical analysis utilities.

Provides:
- ANOVA (one-way and two-way)
- Response Surface analysis
- Main-effects and interaction plots
"""

from doEVC.analysis.anova import one_way_anova, two_way_anova
from doEVC.analysis.response_surface import fit_response_surface
from doEVC.analysis.plots import main_effects_plot, interaction_plot

__all__ = [
    "one_way_anova",
    "two_way_anova",
    "fit_response_surface",
    "main_effects_plot",
    "interaction_plot",
]
