"""Tests for the core DoEVC model metadata."""

from __future__ import annotations

from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from doEVC import ModelParameters, get_version_label


def sample_parameters() -> dict[str, Any]:
    """Return a representative valid parameter set for the tests."""
    return {
        "B0": 10.0,
        "D0": 5.0,
        "V0": 3.0,
        "alpha": 0.2,
        "beta": 0.1,
        "gamma": 0.05,
        "theta": 0.4,
        "lambda_": 0.6,
        "rho": 0.8,
        "K": 12,
    }


def test_version_label_matches_repository_build() -> None:
    """Return the repository version label."""
    assert get_version_label() == "1.0 build 000"


def test_model_parameters_serialize_to_dictionary() -> None:
    """Serialize parameters without losing keys or values."""
    parameters = ModelParameters(**sample_parameters())

    assert parameters.to_dict() == sample_parameters()


@pytest.mark.parametrize(
    "field_name", ["B0", "D0", "V0", "gamma", "theta", "lambda_", "rho"]
)
def test_model_parameters_reject_negative_numeric_values(field_name: str) -> None:
    """Reject negative values for fields that must stay non-negative."""
    data = sample_parameters()
    data[field_name] = -0.1

    with pytest.raises(ValueError, match="must be non-negative"):
        ModelParameters(**data)


@pytest.mark.parametrize("field_name", ["alpha", "beta"])
def test_model_parameters_reject_values_outside_unit_interval(field_name: str) -> None:
    """Reject alpha and beta values outside the accepted interval."""
    data = sample_parameters()
    data[field_name] = 1.1

    with pytest.raises(ValueError, match="must be between 0.0 and 1.0"):
        ModelParameters(**data)


def test_model_parameters_reject_non_positive_sprint_count() -> None:
    """Reject a non-positive sprint count."""
    data = sample_parameters()
    data["K"] = 0

    with pytest.raises(ValueError, match="greater than zero"):
        ModelParameters(**data)


@given(
    b0=st.floats(min_value=0, max_value=100, allow_infinity=False, allow_nan=False),
    d0=st.floats(min_value=0, max_value=100, allow_infinity=False, allow_nan=False),
    v0=st.floats(min_value=0.1, max_value=100, allow_infinity=False, allow_nan=False),
    alpha=st.floats(min_value=0, max_value=1, allow_infinity=False, allow_nan=False),
    beta=st.floats(min_value=0, max_value=1, allow_infinity=False, allow_nan=False),
    gamma=st.floats(min_value=0, max_value=1, allow_infinity=False, allow_nan=False),
    theta=st.floats(min_value=0, max_value=1, allow_infinity=False, allow_nan=False),
    lambda_=st.floats(min_value=0, max_value=1, allow_infinity=False, allow_nan=False),
    rho=st.floats(min_value=0, max_value=1, allow_infinity=False, allow_nan=False),
    k=st.integers(min_value=1, max_value=100),
)
def test_model_parameters_accept_valid_ranges(
    b0: float,
    d0: float,
    v0: float,
    alpha: float,
    beta: float,
    gamma: float,
    theta: float,
    lambda_: float,
    rho: float,
    k: int,
) -> None:
    """Accept values inside the supported ranges."""
    parameters = ModelParameters(
        B0=b0,
        D0=d0,
        V0=v0,
        alpha=alpha,
        beta=beta,
        gamma=gamma,
        theta=theta,
        lambda_=lambda_,
        rho=rho,
        K=k,
    )

    assert parameters.to_dict()["K"] == k
