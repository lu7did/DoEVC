"""Tests for the DoEVC s001 model parameter objects."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from doevc_s001 import ModelParameters


def sample_parameters() -> dict[str, float | int]:
    """Return a representative valid parameter set."""
    return {
        "B0": 100.0,
        "D0": 20.0,
        "V0": 12.0,
        "alpha": 0.3,
        "beta": 0.1,
        "gamma": 0.05,
        "theta": 0.2,
        "lambda_": 0.8,
        "rho": 0.4,
        "K": 16,
    }


def test_model_parameters_serialize_to_dictionary() -> None:
    """Serialize parameters without losing keys or values."""
    parameters = ModelParameters(**sample_parameters())

    assert parameters.to_dict() == sample_parameters()


def test_model_parameters_have_string_representation() -> None:
    """Expose a useful printable representation."""
    parameters = ModelParameters(**sample_parameters())

    assert "ModelParameters" in str(parameters)
    assert "B0=100.0" in str(parameters)


@pytest.mark.parametrize(
    "field_name",
    ["B0", "D0", "V0", "alpha", "beta", "gamma", "theta", "lambda_", "rho"],
)
def test_model_parameters_reject_negative_values(field_name: str) -> None:
    """Reject negative numeric values for the model parameters."""
    data = sample_parameters()
    data[field_name] = -0.1

    with pytest.raises(ValueError, match="must be non-negative"):
        ModelParameters(**data)


def test_model_parameters_reject_non_positive_sprint_count() -> None:
    """Reject a non-positive sprint count."""
    data = sample_parameters()
    data["K"] = 0

    with pytest.raises(ValueError, match="greater than zero"):
        ModelParameters(**data)


@given(
    b0=st.floats(min_value=0, max_value=1_000, allow_infinity=False, allow_nan=False),
    d0=st.floats(min_value=0, max_value=1_000, allow_infinity=False, allow_nan=False),
    v0=st.floats(min_value=0, max_value=1_000, allow_infinity=False, allow_nan=False),
    alpha=st.floats(
        min_value=0, max_value=1_000, allow_infinity=False, allow_nan=False
    ),
    beta=st.floats(min_value=0, max_value=1_000, allow_infinity=False, allow_nan=False),
    gamma=st.floats(
        min_value=0, max_value=1_000, allow_infinity=False, allow_nan=False
    ),
    theta=st.floats(
        min_value=0, max_value=1_000, allow_infinity=False, allow_nan=False
    ),
    lambda_=st.floats(
        min_value=0, max_value=1_000, allow_infinity=False, allow_nan=False
    ),
    rho=st.floats(min_value=0, max_value=1_000, allow_infinity=False, allow_nan=False),
    k=st.integers(min_value=1, max_value=1_000),
)
def test_model_parameters_accept_non_negative_values(
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
    """Accept valid non-negative model parameters."""
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
