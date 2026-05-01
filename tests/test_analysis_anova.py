"""Tests for doEVC.analysis.anova module."""

import numpy as np
import pandas as pd
import pytest

from doEVC.analysis.anova import one_way_anova, two_way_anova


@pytest.fixture()
def simple_one_way():
    """Two clearly different groups."""
    rng = np.random.default_rng(0)
    return pd.DataFrame(
        {
            "group": ["A"] * 10 + ["B"] * 10,
            "y": np.concatenate([rng.normal(5, 0.1, 10), rng.normal(10, 0.1, 10)]),
        }
    )


@pytest.fixture()
def two_way_data():
    rng = np.random.default_rng(1)
    rows = []
    for a in ["low", "high"]:
        for b in ["slow", "fast"]:
            for _ in range(5):
                base = (5 if a == "low" else 10) + (0 if b == "slow" else 2)
                rows.append({"A": a, "B": b, "y": base + rng.normal(0, 0.2)})
    return pd.DataFrame(rows)


class TestOneWayANOVA:
    def test_returns_dataframe(self, simple_one_way):
        result = one_way_anova(simple_one_way, "group", "y")
        assert isinstance(result, pd.DataFrame)

    def test_significant_p_value(self, simple_one_way):
        result = one_way_anova(simple_one_way, "group", "y")
        # Groups are very different → p-value should be tiny
        p = result["PR(>F)"].dropna().iloc[0]
        assert p < 0.01

    def test_has_expected_columns(self, simple_one_way):
        result = one_way_anova(simple_one_way, "group", "y")
        assert "PR(>F)" in result.columns
        assert "F" in result.columns


class TestTwoWayANOVA:
    def test_returns_dataframe(self, two_way_data):
        result = two_way_anova(two_way_data, ["A", "B"], "y")
        assert isinstance(result, pd.DataFrame)

    def test_raises_on_wrong_factor_count(self, two_way_data):
        with pytest.raises(ValueError, match="exactly 2 factors"):
            two_way_anova(two_way_data, ["A"], "y")

    def test_has_expected_rows(self, two_way_data):
        result = two_way_anova(two_way_data, ["A", "B"], "y", interaction=True)
        # Should have rows for A, B, A:B, Residual
        assert len(result) >= 3
