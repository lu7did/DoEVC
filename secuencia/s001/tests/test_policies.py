"""Tests for policy abstractions and deterministic multi-sprint simulation."""

from dataclasses import dataclass

from doevc_s001 import (
    BacklogFirstPolicy,
    DebtFirstPolicy,
    ModelParameters,
    ProportionalDebtPolicy,
    SprintState,
    simulate_deterministic_sprints,
)


def sample_parameters(*, k: int = 8) -> ModelParameters:
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
        effective_velocity=4.0,
        remediation_fraction=0.0,
        feature_capacity=0.0,
        remediation_capacity=0.0,
        next_backlog=backlog,
        next_technical_debt=technical_debt,
    )


def test_debt_first_policy_prioritizes_debt_until_it_reaches_zero() -> None:
    """Return full remediation only while there is technical debt."""
    policy = DebtFirstPolicy()

    assert (
        policy.decide_u(
            sample_state(backlog=10.0, technical_debt=2.0),
            sample_parameters(),
        )
        == 1.0
    )
    assert (
        policy.decide_u(
            sample_state(backlog=10.0, technical_debt=0.0),
            sample_parameters(),
        )
        == 0.0
    )


def test_simulate_deterministic_sprints_uses_debt_first_policy_as_b1_baseline() -> None:
    """Apply the debt-first baseline until debt reaches zero, then resume delivery."""
    trajectory = simulate_deterministic_sprints(
        sample_parameters(k=3),
        DebtFirstPolicy(),
    )

    assert len(trajectory) == 3
    assert trajectory[0].remediation_fraction == 1.0
    assert trajectory[0].next_technical_debt == 0.0
    assert trajectory[1].remediation_fraction == 0.0
    assert trajectory[2].remediation_fraction == 0.0


def test_backlog_first_policy_prioritizes_backlog_then_debt() -> None:
    """Keep delivery first while backlog exists, then switch to debt."""
    policy = BacklogFirstPolicy()

    assert (
        policy.decide_u(
            sample_state(backlog=10.0, technical_debt=2.0),
            sample_parameters(),
        )
        == 0.0
    )
    assert (
        policy.decide_u(
            sample_state(backlog=0.0, technical_debt=2.0),
            sample_parameters(),
        )
        == 1.0
    )
    assert (
        policy.decide_u(
            sample_state(backlog=0.0, technical_debt=0.0),
            sample_parameters(),
        )
        == 0.0
    )


def test_simulate_deterministic_sprints_uses_backlog_first_policy_as_b2_baseline() -> (
    None
):
    """Spend capacity on backlog first, then switch to debt remediation."""
    trajectory = simulate_deterministic_sprints(
        sample_parameters(k=4),
        BacklogFirstPolicy(),
    )

    assert len(trajectory) == 3
    assert trajectory[0].remediation_fraction == 0.0
    assert trajectory[1].remediation_fraction == 0.0
    assert trajectory[1].next_backlog == 0.0
    assert trajectory[2].remediation_fraction == 1.0
    assert trajectory[2].next_technical_debt == 0.0


def test_proportional_debt_policy_handles_edge_cases_and_general_case() -> None:
    """Compute the relative debt fraction without leaving the unit interval."""
    policy = ProportionalDebtPolicy()

    assert (
        policy.decide_u(
            sample_state(backlog=10.0, technical_debt=0.0),
            sample_parameters(),
        )
        == 0.0
    )
    assert (
        policy.decide_u(
            sample_state(backlog=0.0, technical_debt=5.0),
            sample_parameters(),
        )
        == 1.0
    )
    assert (
        policy.decide_u(
            sample_state(backlog=0.0, technical_debt=0.0),
            sample_parameters(),
        )
        == 0.0
    )
    assert (
        policy.decide_u(
            sample_state(backlog=6.0, technical_debt=2.0),
            sample_parameters(),
        )
        == 0.25
    )


@dataclass(slots=True)
class ConstantPolicy:
    """Provide a simple duck-typed policy for integration tests."""

    remediation_fraction: float

    def decide_u(self, state: SprintState, params: ModelParameters) -> float:
        """Return the configured remediation fraction."""
        del state, params
        return self.remediation_fraction


def test_simulate_deterministic_sprints_accepts_policy_protocol_objects() -> None:
    """Accept any duck-typed policy object implementing decide_u()."""
    trajectory = simulate_deterministic_sprints(
        sample_parameters(k=3),
        ConstantPolicy(remediation_fraction=0.5),
    )

    assert len(trajectory) == 3
    assert all(sprint.remediation_fraction == 0.5 for sprint in trajectory)


def test_simulate_deterministic_sprints_stops_early_when_work_is_complete() -> None:
    """Stop before reaching K when both backlog and debt reach zero."""
    parameters = ModelParameters(
        B0=4.0,
        D0=0.0,
        V0=4.0,
        alpha=0.0,
        beta=0.0,
        gamma=0.0,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=10,
        s=1.0,
    )

    trajectory = simulate_deterministic_sprints(parameters, BacklogFirstPolicy())

    assert len(trajectory) == 1
    assert trajectory[-1].next_backlog == 0.0
    assert trajectory[-1].next_technical_debt == 0.0
