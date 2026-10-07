"""Regression tests for model parameters."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from doevc_s002 import ModelParameters


def test_model_parameters_are_serializable_and_printable() -> None:
    """Create a valid parameter set and serialize every accepted field."""
    parameters = ModelParameters(
        B0=100.0,
        D0=20.0,
        V0=10.0,
        alpha=0.5,
        beta=0.2,
        gamma=0.1,
        theta=0.3,
        lambda_=0.8,
        rho=0.4,
        K=12,
    )

    assert parameters.to_dict() == {
        "B0": 100.0,
        "D0": 20.0,
        "V0": 10.0,
        "alpha": 0.5,
        "beta": 0.2,
        "gamma": 0.1,
        "theta": 0.3,
        "lambda_": 0.8,
        "rho": 0.4,
        "K": 12,
        "s": 1.0,
    }
    assert "ModelParameters" in str(parameters)


@pytest.mark.parametrize(
    "field",
    ["B0", "D0", "V0", "alpha", "beta", "gamma", "theta", "lambda_", "rho"],
)
def test_model_parameters_reject_negative_real_values(field: str) -> None:
    """Reject a negative value for every non-negative real parameter."""
    values: dict[str, float | int] = {
        "B0": 1.0,
        "D0": 1.0,
        "V0": 1.0,
        "alpha": 1.0,
        "beta": 1.0,
        "gamma": 1.0,
        "theta": 1.0,
        "lambda_": 1.0,
        "rho": 1.0,
        "K": 1,
    }
    values[field] = -0.1

    with pytest.raises(ValueError, match=field):
        ModelParameters(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [-1, -10])
def test_model_parameters_reject_negative_sprint_counts(value: int) -> None:
    """Reject negative sprint counts."""
    with pytest.raises(ValueError, match="K"):
        ModelParameters(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, value)


@given(
    quantity=st.floats(
        min_value=0,
        max_value=1_000_000,
        allow_nan=False,
        allow_infinity=False,
    ),
    sprint_count=st.integers(min_value=0, max_value=1_000),
)
def test_non_negative_parameters_are_preserved(
    quantity: float, sprint_count: int
) -> None:
    """Preserve every valid generated value in serialized form."""
    parameters = ModelParameters(
        quantity,
        quantity,
        quantity,
        quantity,
        quantity,
        quantity,
        quantity,
        quantity,
        quantity,
        sprint_count,
    )

    assert parameters.to_dict()["B0"] == quantity
    assert parameters.to_dict()["K"] == sprint_count
