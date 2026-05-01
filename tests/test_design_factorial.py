"""Tests for doEVC.design.factorial module."""

import pandas as pd
import pytest

from doEVC.design.factorial import full_factorial, fractional_factorial


class TestFullFactorial:
    def test_shape(self):
        design = full_factorial({"A": [1, 2], "B": [10, 20, 30]})
        assert design.shape == (6, 2), "2-level × 3-level → 6 runs"

    def test_columns(self):
        design = full_factorial({"V_ref": [4.8, 5.0], "load": [10, 100]})
        assert list(design.columns) == ["V_ref", "load"]

    def test_all_combinations_present(self):
        design = full_factorial({"A": [0, 1], "B": [0, 1]})
        expected = {(0, 0), (0, 1), (1, 0), (1, 1)}
        actual = set(map(tuple, design.values.tolist()))
        assert actual == expected

    def test_single_factor(self):
        design = full_factorial({"x": [1, 2, 3]})
        assert len(design) == 3
        assert list(design["x"]) == [1, 2, 3]

    def test_returns_dataframe(self):
        result = full_factorial({"A": [1, 2]})
        assert isinstance(result, pd.DataFrame)


class TestFractionalFactorial:
    def test_four_factor_default(self):
        df = fractional_factorial(4)
        # 2^(4-1) design → 8 runs, 4 columns
        assert df.shape == (8, 4)

    def test_coded_values(self):
        df = fractional_factorial(3)
        unique_vals = set(df.values.flatten())
        assert unique_vals == {-1.0, 1.0}

    def test_column_names(self):
        df = fractional_factorial(3)
        assert list(df.columns) == ["x1", "x2", "x3"]

    def test_returns_dataframe(self):
        result = fractional_factorial(3)
        assert isinstance(result, pd.DataFrame)
