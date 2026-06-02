"""Tests for fixed-grid remediation optimization in DoEVC s001."""

import pytest

from doevc_s001 import (
    EconomicObjectiveFunction,
    FixedRemediationPolicy,
    GridSearchResult,
    ModelParameters,
    search_optimal_remediation_fraction,
    simulate_deterministic_sprints,
)


def sample_parameters() -> ModelParameters:
    """Return a representative parameter set for grid-search tests."""
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
        K=2,
        s=1.0,
    )


def test_fixed_remediation_policy_rejects_invalid_fraction() -> None:
    """Reject remediation fractions outside the closed unit interval."""
    with pytest.raises(ValueError, match="between 0 and 1"):
        FixedRemediationPolicy(1.1)


def test_economic_objective_function_rejects_negative_weights() -> None:
    """Reject negative configuration weights for the economic objective."""
    with pytest.raises(ValueError, match="must be non-negative"):
        EconomicObjectiveFunction(delivered_value_weight=-0.1)


def test_economic_objective_function_scores_known_trajectory() -> None:
    """Score a known deterministic trajectory with the reference formula."""
    parameters = sample_parameters()
    trajectory = simulate_deterministic_sprints(
        parameters,
        FixedRemediationPolicy(0.0),
    )
    objective = EconomicObjectiveFunction(
        delivered_value_weight=1.0,
        residual_debt_penalty_weight=1.0,
        sprint_penalty_weight=1.0,
    )

    assert objective(trajectory, parameters) == pytest.approx(4.4)


def test_search_optimal_remediation_fraction_uses_economic_weights() -> None:
    """Different economic weightings should choose different optimal ``u``."""
    parameters = ModelParameters(
        B0=4.0,
        D0=4.0,
        V0=4.0,
        alpha=0.0,
        beta=0.0,
        gamma=0.0,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=1,
        s=1.0,
    )
    delivered_value_objective = EconomicObjectiveFunction(
        delivered_value_weight=1.0,
        residual_debt_penalty_weight=0.0,
        sprint_penalty_weight=0.0,
    )
    debt_penalty_objective = EconomicObjectiveFunction(
        delivered_value_weight=0.0,
        residual_debt_penalty_weight=1.0,
        sprint_penalty_weight=0.0,
    )

    delivered_result = search_optimal_remediation_fraction(
        parameters,
        objective=delivered_value_objective,
        direction="max",
    )
    debt_result = search_optimal_remediation_fraction(
        parameters,
        objective=debt_penalty_objective,
        direction="max",
    )

    assert isinstance(delivered_result, GridSearchResult)
    assert delivered_result.best_remediation_fraction == 0.0
    assert debt_result.best_remediation_fraction == 1.0
    assert len(delivered_result.evaluations) == 101
    assert len(debt_result.evaluations) == 101


def test_search_optimal_remediation_fraction_supports_configurable_step() -> None:
    """Evaluate the full inclusive grid using the requested step size."""
    result = search_optimal_remediation_fraction(
        sample_parameters(),
        objective=EconomicObjectiveFunction(
            delivered_value_weight=1.0,
            residual_debt_penalty_weight=0.0,
            sprint_penalty_weight=0.0,
        ),
        direction="max",
        step=0.25,
    )

    assert [evaluation.remediation_fraction for evaluation in result.evaluations] == [
        0.0,
        0.25,
        0.5,
        0.75,
        1.0,
    ]


def test_search_optimal_remediation_fraction_forces_zero_when_debt_is_zero() -> None:
    """Return only ``u = 0`` when the current technical debt is already zero."""
    parameters = ModelParameters(
        B0=8.0,
        D0=0.0,
        V0=4.0,
        alpha=0.0,
        beta=0.0,
        gamma=0.0,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=2,
        s=1.0,
    )

    result = search_optimal_remediation_fraction(
        parameters,
        objective=EconomicObjectiveFunction(
            delivered_value_weight=1.0,
            residual_debt_penalty_weight=1.0,
            sprint_penalty_weight=1.0,
        ),
        direction="max",
    )

    assert result.best_remediation_fraction == 0.0
    assert len(result.evaluations) == 1
    assert result.evaluations[0].remediation_fraction == 0.0
