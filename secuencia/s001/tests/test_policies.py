"""Tests for the debt-first baseline policy in DoEVC s001."""

from doevc_s001 import (
    BacklogFirstPolicy,
    DebtFirstPolicy,
    ModelParameters,
    SprintState,
    simulate_deterministic_sprints,
)


def sample_parameters(*, k: int = 4) -> ModelParameters:
    """Return a representative parameter set for policy tests."""
    return ModelParameters(
        B0=8.0,
        D0=4.0,
        V0=4.0,
        alpha=0.0,
        beta=0.0,
        gamma=0.0,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=k,
        s=1.0,
    )


def sample_state(*, backlog: float, technical_debt: float) -> SprintState:
    """Return a lightweight sprint state for policy decisions."""
    return SprintState(
        backlog=backlog,
        technical_debt=technical_debt,
        effective_velocity=0.0,
        remediation_fraction=0.0,
        feature_capacity=0.0,
        remediation_capacity=0.0,
        next_backlog=backlog,
        next_technical_debt=technical_debt,
    )


def test_debt_first_policy_returns_full_remediation_while_debt_exists() -> None:
    """Return full remediation while there is outstanding technical debt."""
    policy = DebtFirstPolicy()

    assert (
        policy.decide_u(
            sample_state(backlog=10.0, technical_debt=2.0),
            sample_parameters(),
        )
        == 1.0
    )


def test_debt_first_policy_returns_zero_when_debt_is_gone() -> None:
    """Return zero remediation once technical debt reaches zero."""
    policy = DebtFirstPolicy()

    assert (
        policy.decide_u(
            sample_state(backlog=10.0, technical_debt=0.0),
            sample_parameters(),
        )
        == 0.0
    )


def test_backlog_first_policy_returns_zero_while_backlog_exists() -> None:
    """Return no remediation while functional backlog remains."""
    policy = BacklogFirstPolicy()

    assert (
        policy.decide_u(
            sample_state(backlog=10.0, technical_debt=2.0),
            sample_parameters(),
        )
        == 0.0
    )


def test_backlog_first_policy_returns_full_remediation_after_backlog_is_gone() -> None:
    """Return full remediation once backlog is gone and debt remains."""
    policy = BacklogFirstPolicy()

    assert (
        policy.decide_u(
            sample_state(backlog=0.0, technical_debt=2.0),
            sample_parameters(),
        )
        == 1.0
    )


def test_simulate_deterministic_sprints_accepts_debt_first_policy() -> None:
    """Integrate the B1 policy with the deterministic multi-sprint simulator."""
    trajectory = simulate_deterministic_sprints(
        sample_parameters(k=3),
        DebtFirstPolicy(),
    )

    assert len(trajectory) == 3
    assert trajectory[0].remediation_fraction == 1.0
    assert trajectory[0].next_technical_debt == 0.0
    assert trajectory[1].remediation_fraction == 0.0
    assert trajectory[2].remediation_fraction == 0.0


def test_simulate_deterministic_sprints_accepts_backlog_first_policy() -> None:
    """Integrate the B2 policy with the deterministic multi-sprint simulator."""
    trajectory = simulate_deterministic_sprints(
        sample_parameters(k=3),
        BacklogFirstPolicy(),
    )

    assert len(trajectory) == 3
    assert trajectory[0].remediation_fraction == 0.0
    assert trajectory[1].remediation_fraction == 0.0
    assert trajectory[2].remediation_fraction == 1.0
    assert trajectory[2].next_technical_debt == 0.0
