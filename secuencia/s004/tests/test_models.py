"""Tests for model parameter structures."""

import pytest

from s004 import ModelParameters


def test_model_parameters_create_and_serialize() -> None:
    """A valid parameter set is immutable and serializable."""
    parameters = ModelParameters(
        B0=1.0,
        D0=0.0,
        V0=2.5,
        alpha=0.1,
        beta=0.2,
        gamma=0.3,
        theta=0.4,
        lambda_=0.5,
        rho=0.6,
        K=10,
    )

    assert parameters.to_dict() == {
        "B0": 1.0,
        "D0": 0.0,
        "V0": 2.5,
        "alpha": 0.1,
        "beta": 0.2,
        "gamma": 0.3,
        "theta": 0.4,
        "lambda_": 0.5,
        "rho": 0.6,
        "K": 10,
        "s": 1.0,
    }


@pytest.mark.parametrize("field_name", ["B0", "D0", "V0", "alpha", "lambda_"])
def test_model_parameters_reject_negative_real_values(field_name: str) -> None:
    """Each real-valued parameter rejects negative values."""
    values: dict[str, float | int] = {
        "B0": 1.0,
        "D0": 0.0,
        "V0": 2.5,
        "alpha": 0.1,
        "beta": 0.2,
        "gamma": 0.3,
        "theta": 0.4,
        "lambda_": 0.5,
        "rho": 0.6,
        "K": 10,
    }
    values[field_name] = -1.0

    with pytest.raises(ValueError, match=f"{field_name} must not be negative"):
        ModelParameters(**values)  # type: ignore[arg-type]


def test_model_parameters_reject_negative_iteration_count() -> None:
    """The iteration count cannot be negative."""
    with pytest.raises(ValueError, match="K must not be negative"):
        ModelParameters(
            B0=1.0,
            D0=0.0,
            V0=2.5,
            alpha=0.1,
            beta=0.2,
            gamma=0.3,
            theta=0.4,
            lambda_=0.5,
            rho=0.6,
            K=-1,
        )


def test_model_parameters_require_positive_base_velocity() -> None:
    """The base velocity must keep effective velocity strictly positive."""
    with pytest.raises(ValueError, match="V0 must be greater than zero"):
        ModelParameters(
            B0=1.0,
            D0=0.0,
            V0=0.0,
            alpha=0.1,
            beta=0.2,
            gamma=0.3,
            theta=0.4,
            lambda_=0.5,
            rho=0.6,
            K=10,
        )
