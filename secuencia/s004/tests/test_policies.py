"""Tests for remediation decision policies."""

from s004 import BacklogFirstPolicy, DebtFirstPolicy, ProportionalPolicy, SprintState
from tests.support import create_parameters


def create_state(technical_debt: float, backlog: float = 100.0) -> SprintState:
    """Return a valid state with the requested technical debt."""
    return SprintState(
        backlog=backlog,
        technical_debt=technical_debt,
        effective_velocity=10.0,
        remediation_fraction=0.0,
        feature_capacity=10.0,
        remediation_capacity=0.0,
        next_backlog=90.0,
        next_technical_debt=technical_debt,
    )


def test_debt_first_policy_remediates_all_existing_debt() -> None:
    """Existing technical debt receives all sprint capacity."""
    policy = DebtFirstPolicy()

    assert policy.decide_u(create_state(technical_debt=1.0), create_parameters()) == 1.0


def test_debt_first_policy_skips_remediation_without_debt() -> None:
    """No remediation capacity is allocated when debt is absent."""
    policy = DebtFirstPolicy()

    assert policy.decide_u(create_state(technical_debt=0.0), create_parameters()) == 0.0


def test_backlog_first_policy_prioritizes_existing_backlog() -> None:
    """Functional backlog receives capacity before technical debt."""
    policy = BacklogFirstPolicy()

    assert (
        policy.decide_u(
            create_state(technical_debt=1.0, backlog=100.0), create_parameters()
        )
        == 0.0
    )


def test_backlog_first_policy_remediates_debt_after_backlog_is_complete() -> None:
    """Debt receives all capacity when the functional backlog is empty."""
    policy = BacklogFirstPolicy()

    assert (
        policy.decide_u(
            create_state(technical_debt=1.0, backlog=0.0),
            create_parameters(),
        )
        == 1.0
    )


def test_proportional_policy_returns_debt_share_of_total_work() -> None:
    """The remediation fraction equals the relative technical debt."""
    policy = ProportionalPolicy()

    assert (
        policy.decide_u(
            create_state(technical_debt=1.0, backlog=3.0),
            create_parameters(),
        )
        == 0.25
    )


def test_proportional_policy_returns_zero_without_debt() -> None:
    """No debt requires no remediation."""
    policy = ProportionalPolicy()

    assert policy.decide_u(create_state(technical_debt=0.0), create_parameters()) == 0.0


def test_proportional_policy_returns_one_when_only_debt_remains() -> None:
    """All capacity remediates debt after the backlog is complete."""
    policy = ProportionalPolicy()

    assert (
        policy.decide_u(
            create_state(technical_debt=1.0, backlog=0.0),
            create_parameters(),
        )
        == 1.0
    )


def test_proportional_policy_handles_empty_state_without_division_by_zero() -> None:
    """An empty state has no remediation allocation."""
    policy = ProportionalPolicy()

    assert (
        policy.decide_u(
            create_state(technical_debt=0.0, backlog=0.0),
            create_parameters(),
        )
        == 0.0
    )
