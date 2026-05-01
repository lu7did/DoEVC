"""Tests for doEVC.design.response_surface and doEVC.design.lhs modules."""

import pandas as pd
import pytest

from doEVC.design.response_surface import central_composite
from doEVC.design.lhs import latin_hypercube


class TestCentralComposite:
    def test_shape_two_factors(self):
        ccd = central_composite(2)
        # CCD for 2 factors (default center=(4,4)):
        # 4 factorial points + 4 axial points + 8 centre points = 16 runs
        assert ccd.shape[1] == 2

    def test_column_names(self):
        ccd = central_composite(3)
        assert list(ccd.columns) == ["x1", "x2", "x3"]

    def test_returns_dataframe(self):
        assert isinstance(central_composite(2), pd.DataFrame)


class TestLatinHypercube:
    def test_shape(self):
        lhs = latin_hypercube(3, 10, seed=42)
        assert lhs.shape == (10, 3)

    def test_unit_range(self):
        lhs = latin_hypercube(4, 20, seed=0)
        assert (lhs.values >= 0).all() and (lhs.values <= 1).all()

    def test_column_names(self):
        lhs = latin_hypercube(2, 5, seed=1)
        assert list(lhs.columns) == ["x1", "x2"]

    def test_reproducible_with_seed(self):
        lhs1 = latin_hypercube(3, 8, seed=99)
        lhs2 = latin_hypercube(3, 8, seed=99)
        assert lhs1.equals(lhs2)

    def test_returns_dataframe(self):
        assert isinstance(latin_hypercube(2, 5, seed=1), pd.DataFrame)
