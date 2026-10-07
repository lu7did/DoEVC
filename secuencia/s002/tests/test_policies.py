"""Regression tests for remediation policies."""

import pytest

from doevc_s002 import DebtFirstPolicy, ModelParameters, simulate_deterministic_sprints


@pytest.mark.parametrize(("debt", "expected"), [(10, 1.0), (0, 0.0)])
def test_debt_first_policy_selects_the_expected_fraction(
    debt: float, expected: float
) -> None:
    """Allocate all capacity to debt only while debt exists."""
    assert DebtFirstPolicy().decide_u(debt) == expected


def test_debt_first_policy_integrates_with_deterministic_simulation() -> None:
    """Choose debt remediation first and feature delivery after debt is cleared."""
    parameters = ModelParameters(10, 5, 10, 0, 0, 0, 0, 0, 0, 2)

    states = simulate_deterministic_sprints(parameters, policy=DebtFirstPolicy())

    assert [state.remediation_fraction for state in states] == [1.0, 0.0]
    assert states[0].next_debt == 0
    assert states[-1].next_backlog == 0
