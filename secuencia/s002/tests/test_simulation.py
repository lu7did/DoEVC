"""Regression tests for deterministic multi-sprint simulations."""

import pytest

from doevc_s002 import ModelParameters, simulate_deterministic_sprints


def _parameters(*, B0: float = 15, D0: float = 0, K: int = 3) -> ModelParameters:
    """Create parameters with an easily verifiable fixed velocity."""
    return ModelParameters(
        B0=B0,
        D0=D0,
        V0=10,
        alpha=0,
        beta=0,
        gamma=0,
        theta=0,
        lambda_=0,
        rho=0,
        K=K,
    )


def test_simulation_returns_the_known_fixed_split_trajectory() -> None:
    """Chain states using the previous sprint's next backlog and debt."""
    states = simulate_deterministic_sprints(_parameters(), remediation_fraction=0.5)

    assert len(states) == 3
    assert [state.backlog for state in states] == [15, 10, 5]
    assert [state.debt for state in states] == [0, 0, 0]
    assert [state.velocity for state in states] == [10, 10, 10]
    assert [state.remediation_fraction for state in states] == [0.5, 0.5, 0.5]
    assert [state.feature_capacity for state in states] == [5, 5, 5]
    assert [state.remediation_capacity for state in states] == [5, 5, 5]
    assert states[-1].next_backlog == 0


def test_simulation_stops_when_all_work_is_finished() -> None:
    """Stop instead of emitting empty sprints after both quantities reach zero."""
    states = simulate_deterministic_sprints(
        _parameters(B0=5, D0=0, K=10), remediation_fraction=0
    )

    assert len(states) == 1
    assert states[0].next_backlog == 0
    assert states[0].next_debt == 0


def test_simulation_returns_no_states_when_initial_work_is_zero() -> None:
    """Avoid a sprint when the initial model state is already complete."""
    states = simulate_deterministic_sprints(
        _parameters(B0=0, D0=0, K=10), remediation_fraction=0.5
    )

    assert states == []


@pytest.mark.parametrize("fraction", [-0.1, 1.1])
def test_simulation_rejects_invalid_fixed_fractions(fraction: float) -> None:
    """Validate the fixed fraction even when the model has no sprints."""
    with pytest.raises(ValueError, match="remediation_fraction"):
        simulate_deterministic_sprints(_parameters(K=0), fraction)
