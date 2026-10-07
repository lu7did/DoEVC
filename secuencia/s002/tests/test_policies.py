"""Regression tests for remediation policies."""

import pytest

from doevc_s002 import (
    BacklogFirstPolicy,
    DebtFirstPolicy,
    ModelParameters,
    simulate_deterministic_sprints,
)


@pytest.mark.parametrize(("debt", "expected"), [(10, 1.0), (0, 0.0)])
def test_debt_first_policy_selects_the_expected_fraction(
    debt: float, expected: float
) -> None:
    """Allocate all capacity to debt only while debt exists."""
    assert DebtFirstPolicy().decide_u(10, debt) == expected


def test_debt_first_policy_integrates_with_deterministic_simulation() -> None:
    """Choose debt remediation first and feature delivery after debt is cleared."""
    parameters = ModelParameters(10, 5, 10, 0, 0, 0, 0, 0, 0, 2)

    states = simulate_deterministic_sprints(parameters, policy=DebtFirstPolicy())

    assert [state.remediation_fraction for state in states] == [1.0, 0.0]
    assert states[0].next_debt == 0
    assert states[-1].next_backlog == 0


@pytest.mark.parametrize(
    ("backlog", "debt", "expected"), [(10, 5, 0.0), (0, 5, 1.0), (0, 0, 0.0)]
)
def test_backlog_first_policy_selects_the_expected_fraction(
    backlog: float, debt: float, expected: float
) -> None:
    """Deliver backlog before remediating remaining debt."""
    assert BacklogFirstPolicy().decide_u(backlog, debt) == expected


def test_backlog_first_policy_integrates_with_deterministic_simulation() -> None:
    """Choose feature work first and debt remediation after backlog is cleared."""
    parameters = ModelParameters(10, 5, 10, 0, 0, 0, 0, 0, 0, 2)

    states = simulate_deterministic_sprints(parameters, policy=BacklogFirstPolicy())

    assert [state.remediation_fraction for state in states] == [0.0, 1.0]
    assert states[0].next_backlog == 0
    assert states[-1].next_debt == 0
