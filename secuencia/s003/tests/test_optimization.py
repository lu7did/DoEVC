"""Regression tests for fixed-allocation grid search in s003."""

from doevc_s003 import (
    BacklogFirstPolicy,
    EconomicObjective,
    ModelParameters,
    OptimalLocalPolicy,
    Policy,
    SprintState,
    find_optimal_allocation,
    simulate_sprints,
)


def _parameters() -> ModelParameters:
    """Create a one-sprint scenario with opposite backlog objectives."""
    return ModelParameters(10, 0, 10, 0, 0, 0, 0, 0, 0, 1)


def _final_backlog(trajectory: list[SprintState]) -> float:
    """Return the final backlog for a guaranteed non-empty trajectory."""
    return trajectory[-1].next_backlog


def test_grid_search_finds_the_allocation_that_minimizes_final_backlog() -> None:
    """Prefer full delivery when the objective is terminal backlog."""
    optimal_allocation = find_optimal_allocation(
        _parameters(), _final_backlog, step=0.25
    )

    assert optimal_allocation == 0


def test_grid_search_can_maximize_a_configurable_objective() -> None:
    """Prefer full remediation when maximizing terminal backlog."""
    optimal_allocation = find_optimal_allocation(
        _parameters(), _final_backlog, step=0.25, maximize=True
    )

    assert optimal_allocation == 1


def test_grid_search_evaluates_every_inclusive_grid_value() -> None:
    """Run one complete deterministic simulation for each configured value."""
    evaluated_allocations: list[float] = []

    def record_allocation(trajectory: list[SprintState]) -> float:
        """Record the fixed allocation supplied to this simulation."""
        evaluated_allocations.append(trajectory[0].allocation)
        return 0

    find_optimal_allocation(_parameters(), record_allocation, step=0.25)

    assert evaluated_allocations == [0, 0.25, 0.5, 0.75, 1]


def test_economic_objective_calculates_weighted_trajectory_value() -> None:
    """Combine delivered work, final debt, and consumed sprints into one score."""
    trajectory = [SprintState(10, 5, 0.2, 5, 1, 4, 7, 3)]

    value = EconomicObjective(2, 4, 0.5)(trajectory)

    assert value == -6.5


def test_economic_weights_produce_distinct_optimal_allocations() -> None:
    """Change the selected allocation when debt becomes more valuable than delivery."""
    parameters = ModelParameters(10, 10, 10, 0, 0, 0, 0, 0, 0, 1)

    delivery_optimum = find_optimal_allocation(
        parameters,
        EconomicObjective(delivery_weight=2, debt_weight=0.5),
        step=0.25,
        maximize=True,
    )
    debt_optimum = find_optimal_allocation(
        parameters,
        EconomicObjective(delivery_weight=1, debt_weight=2),
        step=0.25,
        maximize=True,
    )

    assert delivery_optimum == 0
    assert debt_optimum == 1


def test_optimal_local_policy_evaluates_the_grid_for_each_decision() -> None:
    """Use D1's full candidate grid from the state supplied by the engine."""
    evaluations: list[float] = []

    def record_allocation(trajectory: list[SprintState]) -> float:
        """Record each allocation evaluated by the local policy."""
        evaluations.append(trajectory[0].allocation)
        return trajectory[0].allocation

    policy = OptimalLocalPolicy(record_allocation, step=0.25)

    allocation = policy.decide_u(SprintState.current(10, 0), _parameters())

    assert allocation == 1
    assert evaluations == [0, 0.25, 0.5, 0.75, 1]


def test_optimal_local_policy_beats_a_heuristic_in_a_known_scenario() -> None:
    """Exchange the local policy in the engine and improve the debt-weighted value."""
    parameters = ModelParameters(10, 10, 10, 0, 0, 0, 0, 0, 0, 1)
    objective = EconomicObjective(delivery_weight=1, debt_weight=2)
    policy = OptimalLocalPolicy(objective, step=0.25)

    optimized_trajectory = simulate_sprints(parameters, policy)
    heuristic_trajectory = simulate_sprints(parameters, BacklogFirstPolicy())

    assert isinstance(policy, Policy)
    assert optimized_trajectory[0].allocation == 1
    assert objective(optimized_trajectory) > objective(heuristic_trajectory)
