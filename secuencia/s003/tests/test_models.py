"""Regression tests for s003 model parameters."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from doevc_s003 import ModelParameters


def test_model_parameters_serialize_all_supported_fields() -> None:
    """Create printable, immutable parameters with a complete mapping."""
    parameters = ModelParameters(10, 2, 5, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 7)

    assert parameters.to_dict()["B0"] == 10
    assert parameters.to_dict()["K"] == 7
    assert "ModelParameters" in str(parameters)


@pytest.mark.parametrize(
    "field_name",
    ["B0", "D0", "V0", "alpha", "beta", "gamma", "theta", "lambda_", "rho"],
)
def test_negative_real_parameters_are_rejected(field_name: str) -> None:
    """Reject every negative real-valued model input."""
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
    values[field_name] = -0.1

    with pytest.raises(ValueError, match=field_name):
        ModelParameters(**values)  # type: ignore[arg-type]


@given(st.floats(min_value=0, max_value=1_000, allow_nan=False))
def test_non_negative_values_are_preserved(value: float) -> None:
    """Preserve valid generated values in the serialized result."""
    parameters = ModelParameters(
        value, value, value, value, value, value, value, value, value, 1
    )

    assert parameters.to_dict()["alpha"] == value
