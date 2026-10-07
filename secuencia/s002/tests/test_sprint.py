"""Regression tests for deterministic sprint transitions."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from doevc_s002 import ModelParameters, SprintState, simulate_sprint


def _parameters() -> ModelParameters:
    """Create a representative valid parameter set."""
    return ModelParameters(
        B0=100.0,
        D0=20.0,
        V0=10.0,
        alpha=0.1,
        beta=0.2,
        gamma=0.1,
        theta=0.3,
        lambda_=0.8,
        rho=0.4,
        K=12,
    )


def test_simulate_sprint_uses_the_documented_equations() -> None:
    """Calculate the known next state for a fixed remediation split."""
    state = simulate_sprint(
        _parameters(), backlog=100, debt=20, remediation_fraction=0.5
    )

    assert isinstance(state, SprintState)
    assert state.velocity == pytest.approx(10 / 3)
    assert state.remediation_capacity == pytest.approx(5 / 3)
    assert state.feature_capacity == pytest.approx(5 / 3)
    assert state.next_backlog == pytest.approx(100 - 5 / 3)
    assert state.next_debt == pytest.approx(20 - 5 / 3 + 1 / 6 + 1 / 3)


@pytest.mark.parametrize("fraction", [-0.1, 1.1])
def test_simulate_sprint_rejects_out_of_range_fractions(fraction: float) -> None:
    """Reject a remediation fraction outside the closed unit interval."""
    with pytest.raises(ValueError, match="remediation_fraction"):
        simulate_sprint(_parameters(), 100, 20, fraction)


def test_simulate_sprint_clamps_backlog_and_debt_to_zero() -> None:
    """Avoid negative state values when a sprint exceeds remaining work."""
    parameters = ModelParameters(
        B0=1,
        D0=1,
        V0=10,
        alpha=0,
        beta=0,
        gamma=0,
        theta=0,
        lambda_=0,
        rho=0,
        K=1,
    )

    state = simulate_sprint(parameters, backlog=1, debt=1, remediation_fraction=0.5)

    assert state.next_backlog == 0
    assert state.next_debt == 0
    assert state.to_dict()["next_backlog"] == 0


@given(
    backlog=st.floats(
        min_value=0, max_value=1_000_000, allow_nan=False, allow_infinity=False
    ),
    debt=st.floats(
        min_value=0, max_value=1_000_000, allow_nan=False, allow_infinity=False
    ),
    fraction=st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
)
def test_simulate_sprint_never_returns_negative_work(
    backlog: float, debt: float, fraction: float
) -> None:
    """Maintain non-negative backlog and debt for every valid split."""
    state = simulate_sprint(_parameters(), backlog, debt, fraction)

    assert state.next_backlog >= 0
    assert state.next_debt >= 0
