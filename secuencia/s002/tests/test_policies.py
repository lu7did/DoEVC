"""Regression tests for remediation policies."""

import pytest

from doevc_s002 import (
    BacklogFirstPolicy,
    DebtFirstPolicy,
    ModelParameters,
    ProportionalPolicy,
    SprintState,
    simulate_deterministic_sprints,
)


def _state(backlog: float, debt: float) -> SprintState:
    """Create the current-state view provided to a policy."""
    return SprintState(backlog, debt, 1, 0, 0, 0, backlog, debt)


@pytest.mark.parametrize(("debt", "expected"), [(10, 1.0), (0, 0.0)])
def test_debt_first_policy_selects_the_expected_fraction(
    debt: float, expected: float
) -> None:
    """Allocate all capacity to debt only while debt exists."""
    assert (
        DebtFirstPolicy().decide_u(
            _state(10, debt), ModelParameters(0, 0, 1, 0, 0, 0, 0, 0, 0, 1)
        )
        == expected
    )


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
    assert (
        BacklogFirstPolicy().decide_u(
            _state(backlog, debt), ModelParameters(0, 0, 1, 0, 0, 0, 0, 0, 0, 1)
        )
        == expected
    )


def test_backlog_first_policy_integrates_with_deterministic_simulation() -> None:
    """Choose feature work first and debt remediation after backlog is cleared."""
    parameters = ModelParameters(10, 5, 10, 0, 0, 0, 0, 0, 0, 2)

    states = simulate_deterministic_sprints(parameters, policy=BacklogFirstPolicy())

    assert [state.remediation_fraction for state in states] == [0.0, 1.0]
    assert states[0].next_backlog == 0
    assert states[-1].next_debt == 0


@pytest.mark.parametrize(
    ("backlog", "debt", "expected"),
    [(10, 0, 0.0), (0, 10, 1.0), (0, 0, 0.0), (3, 1, 0.25)],
)
def test_proportional_policy_handles_general_and_edge_cases(
    backlog: float, debt: float, expected: float
) -> None:
    """Choose the debt share of remaining work without division by zero."""
    result = ProportionalPolicy().decide_u(
        _state(backlog, debt), ModelParameters(0, 0, 1, 0, 0, 0, 0, 0, 0, 1)
    )

    assert result == expected
    assert 0 <= result <= 1


def test_proportional_policy_integrates_with_deterministic_simulation() -> None:
    """Use the proportional fraction in every deterministic sprint."""
    parameters = ModelParameters(6, 2, 4, 0, 0, 0, 0, 0, 0, 1)

    states = simulate_deterministic_sprints(parameters, policy=ProportionalPolicy())

    assert states[0].remediation_fraction == pytest.approx(0.25)


@pytest.mark.parametrize(
    "policy", [DebtFirstPolicy(), BacklogFirstPolicy(), ProportionalPolicy()]
)
def test_every_policy_is_interchangeable_in_the_simulator(policy: object) -> None:
    """Accept each B-series policy without concrete simulator coupling."""
    parameters = ModelParameters(2, 2, 2, 0, 0, 0, 0, 0, 0, 1)

    assert len(simulate_deterministic_sprints(parameters, policy=policy)) == 1
