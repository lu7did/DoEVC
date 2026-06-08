"""Tests for fixed-grid remediation optimization in DoEVC s001."""

import pytest

from doevc_s001 import (
    BacklogFirstPolicy,
    DebtFirstPolicy,
    EconomicObjectiveFunction,
    FixedRemediationPolicy,
    GridSearchEvaluation,
    GridSearchResult,
    ModelParameters,
    OptimalLocalPolicy,
    Policy,
    ProportionalDebtPolicy,
    SprintState,
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


def sample_policy_state(*, backlog: float, technical_debt: float) -> SprintState:
    """Return a representative state for policy-level optimization tests."""
    return SprintState(
        backlog=backlog,
        technical_debt=technical_debt,
        effective_velocity=4.0,
        remediation_fraction=0.0,
        feature_capacity=0.0,
        remediation_capacity=0.0,
        next_backlog=backlog,
        next_technical_debt=technical_debt,
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


def test_optimal_local_policy_is_interchangeable_with_policy_protocol() -> None:
    """Expose the local optimizer as a regular policy implementation."""
    objective = EconomicObjectiveFunction(
        delivered_value_weight=1.0,
        residual_debt_penalty_weight=1.0,
        sprint_penalty_weight=0.0,
    )
    policy = OptimalLocalPolicy(objective=objective, step=0.25)

    trajectory = simulate_deterministic_sprints(sample_parameters(), policy)

    assert isinstance(policy, Policy)
    assert len(trajectory) == 2
    assert all(0.0 <= sprint.remediation_fraction <= 1.0 for sprint in trajectory)


def test_optimal_local_policy_matches_grid_search_for_current_state() -> None:
    """Choose the same fraction as the local grid search over the current state."""
    parameters = sample_parameters()
    objective = EconomicObjectiveFunction(
        delivered_value_weight=1.0,
        residual_debt_penalty_weight=1.0,
        sprint_penalty_weight=0.0,
    )
    policy = OptimalLocalPolicy(objective=objective, step=0.25)
    state = sample_policy_state(backlog=4.0, technical_debt=2.0)

    decision = policy.decide_u(state, parameters)
    expected = search_optimal_remediation_fraction(
        parameters,
        objective,
        direction="max",
        step=0.25,
        backlog=state.backlog,
        technical_debt=state.technical_debt,
    )

    assert decision == expected.best_remediation_fraction == 0.25


def test_optimal_local_policy_forces_zero_when_debt_is_zero() -> None:
    """Return zero remediation immediately when there is no debt to remove."""
    policy = OptimalLocalPolicy(
        objective=EconomicObjectiveFunction(),
        step=0.25,
    )

    decision = policy.decide_u(
        sample_policy_state(backlog=4.0, technical_debt=0.0),
        sample_parameters(),
    )

    assert decision == 0.0


def test_optimal_local_policy_rejects_invalid_direction() -> None:
    """Reject unsupported optimization directions at construction time."""
    with pytest.raises(ValueError, match="either 'min' or 'max'"):
        OptimalLocalPolicy(
            objective=EconomicObjectiveFunction(),
            direction="median",  # type: ignore[arg-type]
        )


def test_optimal_local_policy_rejects_invalid_step() -> None:
    """Reject invalid grid steps at construction time."""
    with pytest.raises(ValueError, match="greater than 0 and at most 1"):
        OptimalLocalPolicy(
            objective=EconomicObjectiveFunction(),
            step=0.0,
        )


def test_optimal_local_policy_beats_a_heuristic_in_known_scenario() -> None:
    """Outperform at least one baseline heuristic in a scenario with debt growth."""
    parameters = ModelParameters(
        B0=4.0,
        D0=2.0,
        V0=3.0,
        alpha=0.2,
        beta=0.0,
        gamma=0.0,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=3,
        s=1.0,
    )
    objective = EconomicObjectiveFunction(
        delivered_value_weight=1.0,
        residual_debt_penalty_weight=1.0,
        sprint_penalty_weight=0.0,
    )
    optimal_trajectory = simulate_deterministic_sprints(
        parameters,
        OptimalLocalPolicy(objective=objective, step=0.25),
    )
    debt_first_trajectory = simulate_deterministic_sprints(
        parameters,
        DebtFirstPolicy(),
    )
    backlog_first_trajectory = simulate_deterministic_sprints(
        parameters,
        BacklogFirstPolicy(),
    )
    proportional_trajectory = simulate_deterministic_sprints(
        parameters,
        ProportionalDebtPolicy(),
    )

    optimal_score = objective(optimal_trajectory, parameters)

    assert optimal_trajectory[0].remediation_fraction == pytest.approx(0.5)
    assert optimal_score > objective(debt_first_trajectory, parameters)
    assert optimal_score == pytest.approx(
        objective(backlog_first_trajectory, parameters)
    )
    assert optimal_score < objective(proportional_trajectory, parameters)


def test_search_optimal_remediation_fraction_supports_min_direction() -> None:
    """Select the lowest objective value when minimizing."""
    result = search_optimal_remediation_fraction(
        sample_parameters(),
        objective=EconomicObjectiveFunction(
            delivered_value_weight=1.0,
            residual_debt_penalty_weight=0.0,
            sprint_penalty_weight=0.0,
        ),
        direction="min",
        step=0.5,
    )

    assert result.best_remediation_fraction == 1.0
    assert result.best_evaluation.remediation_fraction == 1.0


def test_search_optimal_remediation_fraction_rejects_invalid_direction() -> None:
    """Reject directions outside the supported min/max values."""
    with pytest.raises(ValueError, match="either 'min' or 'max'"):
        search_optimal_remediation_fraction(
            sample_parameters(),
            objective=EconomicObjectiveFunction(),
            direction="median",  # type: ignore[arg-type]
        )


def test_search_optimal_remediation_fraction_rejects_invalid_step() -> None:
    """Reject step sizes outside the open-closed interval ``(0, 1]``."""
    with pytest.raises(ValueError, match="greater than 0 and at most 1"):
        search_optimal_remediation_fraction(
            sample_parameters(),
            objective=EconomicObjectiveFunction(),
            step=0.0,
        )


def test_search_optimal_remediation_fraction_appends_terminal_one_to_grid() -> None:
    """Always include ``1.0`` even when the step does not land on it exactly."""
    result = search_optimal_remediation_fraction(
        sample_parameters(),
        objective=EconomicObjectiveFunction(),
        step=0.3,
    )

    assert [evaluation.remediation_fraction for evaluation in result.evaluations] == [
        0.0,
        0.3,
        0.6,
        0.9,
        1.0,
    ]


def test_grid_search_result_best_evaluation_requires_matching_entry() -> None:
    """Raise a clear error when the recorded best fraction is missing."""
    result = GridSearchResult(
        best_remediation_fraction=0.75,
        best_objective_value=1.0,
        evaluations=(
            GridSearchEvaluation(
                remediation_fraction=0.25,
                objective_value=1.0,
                trajectory=(),
            ),
        ),
    )

    with pytest.raises(RuntimeError, match="best evaluation is missing"):
        _ = result.best_evaluation
