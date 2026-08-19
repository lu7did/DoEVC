"""Tests for deterministic multi-sprint simulation in DoEVC s001."""

import math

from doevc_s001 import ModelParameters, SprintState, simulate_deterministic_sprints


def sample_parameters() -> ModelParameters:
    """Return a representative parameter set for deterministic simulation tests."""
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
        K=3,
        s=1.0,
    )


def test_simulate_deterministic_sprints_returns_known_fixed_u_trajectory() -> None:
    """Return the expected sprint-by-sprint trajectory for a fixed split."""
    states = simulate_deterministic_sprints(
        sample_parameters(),
        remediation_fraction=0.25,
    )

    assert len(states) == 3
    assert all(isinstance(state, SprintState) for state in states)

    first, second, third = states
    assert math.isclose(first.backlog, 100.0)
    assert math.isclose(first.technical_debt, 20.0)
    assert math.isclose(first.effective_velocity, 6.0)
    assert math.isclose(first.remediation_fraction, 0.25)
    assert math.isclose(first.feature_capacity, 4.5)
    assert math.isclose(first.remediation_capacity, 1.5)
    assert math.isclose(first.next_backlog, 95.5)
    assert math.isclose(first.next_technical_debt, 20.0)

    assert math.isclose(second.backlog, first.next_backlog)
    assert math.isclose(second.technical_debt, first.next_technical_debt)
    assert math.isclose(second.next_backlog, 91.0)
    assert math.isclose(second.next_technical_debt, 20.0)

    assert math.isclose(third.backlog, second.next_backlog)
    assert math.isclose(third.technical_debt, second.next_technical_debt)
    assert math.isclose(third.next_backlog, 86.5)
    assert math.isclose(third.next_technical_debt, 20.0)


def test_simulate_deterministic_sprints_stops_when_work_is_already_done() -> None:
    """Stop immediately when backlog and debt both start at zero."""
    states = simulate_deterministic_sprints(
        sample_parameters(),
        remediation_fraction=0.25,
        backlog=0.0,
        technical_debt=0.0,
    )

    assert states == ()


def test_simulate_deterministic_sprints_stops_early_after_clearing_work() -> None:
    """Stop before reaching K once both backlog and debt reach zero."""
    parameters = ModelParameters(
        B0=2.0,
        D0=1.0,
        V0=10.0,
        alpha=0.0,
        beta=0.0,
        gamma=0.0,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=5,
        s=1.0,
    )

    states = simulate_deterministic_sprints(parameters, remediation_fraction=0.5)

    assert len(states) == 1
    assert math.isclose(states[-1].next_backlog, 0.0)
    assert math.isclose(states[-1].next_technical_debt, 0.0)


def test_simulate_deterministic_sprints_can_start_from_custom_state() -> None:
    """Use explicit initial backlog and debt instead of B0 and D0."""
    states = simulate_deterministic_sprints(
        sample_parameters(),
        remediation_fraction=0.0,
        backlog=10.0,
        technical_debt=5.0,
    )

    assert math.isclose(states[0].backlog, 10.0)
    assert math.isclose(states[0].technical_debt, 5.0)
