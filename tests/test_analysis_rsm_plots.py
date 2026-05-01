"""Tests for doEVC.analysis.response_surface and doEVC.analysis.plots."""

import numpy as np
import pandas as pd
import pytest
import matplotlib

matplotlib.use("Agg")  # non-interactive backend for tests

from doEVC.analysis.response_surface import fit_response_surface
from doEVC.analysis.plots import main_effects_plot, interaction_plot
from doEVC.design.response_surface import central_composite


@pytest.fixture()
def ccd_with_response():
    design = central_composite(2, center=(3, 3))
    # Synthetic quadratic response: y = 1 - x1^2 - x2^2 + noise
    rng = np.random.default_rng(42)
    y = 1.0 - design["x1"] ** 2 - design["x2"] ** 2 + rng.normal(0, 0.05, len(design))
    return design, y


class TestFitResponseSurface:
    def test_returns_results(self, ccd_with_response):
        design, y = ccd_with_response
        result = fit_response_surface(design, y, order=2)
        assert result is not None

    def test_r_squared_reasonable(self, ccd_with_response):
        design, y = ccd_with_response
        result = fit_response_surface(design, y, order=2)
        assert result.rsquared > 0.9

    def test_invalid_order_raises(self, ccd_with_response):
        design, y = ccd_with_response
        with pytest.raises(ValueError, match="order must be 1 or 2"):
            fit_response_surface(design, y, order=3)

    def test_linear_order(self, ccd_with_response):
        design, y = ccd_with_response
        result = fit_response_surface(design, y, order=1)
        assert result is not None


class TestPlots:
    @pytest.fixture()
    def factorial_data(self):
        rows = []
        for v in [4.8, 5.0, 5.2]:
            for l in [10, 100]:
                for _ in range(3):
                    rows.append({"V_ref": v, "load": l, "V_out": v * 0.99 - l * 0.001})
        return pd.DataFrame(rows)

    def test_main_effects_plot_returns_figure(self, factorial_data):
        fig = main_effects_plot(factorial_data, ["V_ref", "load"], "V_out")
        import matplotlib.pyplot as plt
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_interaction_plot_returns_figure(self, factorial_data):
        fig = interaction_plot(factorial_data, "V_ref", "load", "V_out")
        import matplotlib.pyplot as plt
        assert isinstance(fig, plt.Figure)
        plt.close(fig)
