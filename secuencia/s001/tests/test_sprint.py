"""Tests for one-sprint deterministic simulation in DoEVC s001."""

import math

import pytest
from hypothesis import given
from hypothesis import strategies as st

from doevc_s001 import ModelParameters, SprintState, simulate_sprint


def sample_parameters() -> ModelParameters:
    """Return a representative parameter set for sprint tests."""
    return ModelParameters(
        B0=100.0,
        D0=20.0,
        V0=12.0,
        alpha=0.3,
        beta=0.1,
        gamma=0.05,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=16,
        s=1.0,
    )


def test_simulate_sprint_returns_state_with_expected_transitions() -> None:
    """Return the next sprint state following the analytical update rules."""
    state = simulate_sprint(
        sample_parameters(),
        backlog=100.0,
        technical_debt=20.0,
        remediation_fraction=0.25,
    )

    assert isinstance(state, SprintState)
    assert math.isclose(state.effective_velocity, 6.0)
    assert math.isclose(state.remediation_capacity, 1.5)
    assert math.isclose(state.feature_capacity, 4.5)
    assert math.isclose(state.next_backlog, 95.5)
    assert math.isclose(state.next_technical_debt, 20.0)
    assert state.to_dict()["next_technical_debt"] == state.next_technical_debt


def test_simulate_sprint_never_returns_negative_backlog() -> None:
    """Clamp the next backlog to zero when the sprint clears it."""
    state = simulate_sprint(
        sample_parameters(),
        backlog=2.0,
        technical_debt=0.0,
        remediation_fraction=0.0,
    )

    assert state.next_backlog == 0.0


def test_simulate_sprint_never_returns_negative_technical_debt() -> None:
    """Clamp the next technical debt to zero when remediation overshoots it."""
    parameters = ModelParameters(
        B0=100.0,
        D0=20.0,
        V0=10.0,
        alpha=0.0,
        beta=0.0,
        gamma=0.0,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=16,
        s=1.0,
    )

    state = simulate_sprint(
        parameters,
        backlog=100.0,
        technical_debt=1.0,
        remediation_fraction=1.0,
    )

    assert state.next_technical_debt == 0.0


@pytest.mark.parametrize("remediation_fraction", [-0.1, 1.1])
def test_simulate_sprint_rejects_invalid_remediation_fraction(
    remediation_fraction: float,
) -> None:
    """Reject fractions that fall outside the closed unit interval."""
    with pytest.raises(ValueError, match="between 0 and 1"):
        simulate_sprint(
            sample_parameters(),
            backlog=100.0,
            technical_debt=20.0,
            remediation_fraction=remediation_fraction,
        )


@pytest.mark.parametrize("field_name", ["backlog", "technical_debt"])
def test_sprint_state_rejects_negative_values(field_name: str) -> None:
    """Reject negative stored values in the sprint state model."""
    data = {
        "backlog": 100.0,
        "technical_debt": 20.0,
        "effective_velocity": 6.0,
        "remediation_fraction": 0.25,
        "feature_capacity": 4.5,
        "remediation_capacity": 1.5,
        "next_backlog": 95.5,
        "next_technical_debt": 19.0,
    }
    data[field_name] = -0.1

    with pytest.raises(ValueError, match="must be non-negative"):
        SprintState(**data)


@given(
    v0=st.floats(min_value=0.1, max_value=1_000, allow_nan=False, allow_infinity=False),
    gamma=st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
    alpha=st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
    beta=st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
    backlog=st.floats(
        min_value=0, max_value=1_000, allow_nan=False, allow_infinity=False
    ),
    technical_debt=st.floats(
        min_value=0, max_value=1_000, allow_nan=False, allow_infinity=False
    ),
    remediation_fraction=st.floats(
        min_value=0, max_value=1, allow_nan=False, allow_infinity=False
    ),
)
def test_simulate_sprint_respects_acceptance_invariants(
    v0: float,
    gamma: float,
    alpha: float,
    beta: float,
    backlog: float,
    technical_debt: float,
    remediation_fraction: float,
) -> None:
    """Keep the updated sprint state inside the accepted bounds."""
    parameters = ModelParameters(
        B0=100.0,
        D0=20.0,
        V0=v0,
        alpha=alpha,
        beta=beta,
        gamma=gamma,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=16,
        s=1.0,
    )

    state = simulate_sprint(
        parameters,
        backlog=backlog,
        technical_debt=technical_debt,
        remediation_fraction=remediation_fraction,
    )

    assert 0.0 <= state.remediation_fraction <= 1.0
    assert state.next_backlog >= 0.0
    assert state.next_technical_debt >= 0.0
