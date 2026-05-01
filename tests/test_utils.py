"""Tests for doEVC.utils modules."""

import os
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from doEVC.utils.io import load_csv, save_csv
from doEVC.utils.reproducibility import set_seed


class TestIO:
    def test_save_and_load_roundtrip(self, tmp_path):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4.0, 5.0, 6.0]})
        path = tmp_path / "test.csv"
        save_csv(df, path)
        loaded = load_csv(path)
        pd.testing.assert_frame_equal(df, loaded)

    def test_save_creates_parent_dirs(self, tmp_path):
        df = pd.DataFrame({"x": [1]})
        path = tmp_path / "sub" / "dir" / "data.csv"
        save_csv(df, path)
        assert path.exists()

    def test_load_accepts_pathlib(self, tmp_path):
        df = pd.DataFrame({"v": [10, 20]})
        p = tmp_path / "data.csv"
        df.to_csv(p, index=False)
        loaded = load_csv(p)
        assert list(loaded["v"]) == [10, 20]


class TestReproducibility:
    def test_set_seed_numpy(self):
        set_seed(7)
        a = np.random.rand(5)
        set_seed(7)
        b = np.random.rand(5)
        np.testing.assert_array_equal(a, b)

    def test_set_seed_python_random(self):
        import random
        set_seed(42)
        a = [random.random() for _ in range(10)]
        set_seed(42)
        b = [random.random() for _ in range(10)]
        assert a == b
