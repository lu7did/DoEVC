"""Tests for remediation decision policies."""

from s004 import DebtFirstPolicy, SprintState
from tests.support import create_parameters


def create_state(technical_debt: float) -> SprintState:
    """Return a valid state with the requested technical debt."""
    return SprintState(
        backlog=100.0,
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
