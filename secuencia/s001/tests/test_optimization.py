"""Tests for fixed-grid remediation optimization in DoEVC s001."""

import pytest

from doevc_s001 import (
    FixedRemediationPolicy,
    GridSearchResult,
    ModelParameters,
    search_optimal_remediation_fraction,
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


def test_search_optimal_remediation_fraction_minimizes_known_objective() -> None:
    """Find the fixed remediation fraction that minimizes final backlog."""
    result = search_optimal_remediation_fraction(
        sample_parameters(),
        objective=lambda trajectory, params: (
            params.B0 if not trajectory else trajectory[-1].next_backlog
        ),
    )

    assert isinstance(result, GridSearchResult)
    assert result.best_remediation_fraction == 0.0
    assert result.best_objective_value == 0.0
    assert len(result.evaluations) == 101


def test_search_optimal_remediation_fraction_maximizes_known_objective() -> None:
    """Find the fixed remediation fraction that maximizes final backlog."""
    result = search_optimal_remediation_fraction(
        sample_parameters(),
        objective=lambda trajectory, params: (
            params.B0 if not trajectory else trajectory[-1].next_backlog
        ),
        direction="max",
    )

    assert result.best_remediation_fraction == 1.0
    assert result.best_objective_value == 8.0


def test_search_optimal_remediation_fraction_supports_configurable_step() -> None:
    """Evaluate the full inclusive grid using the requested step size."""
    result = search_optimal_remediation_fraction(
        sample_parameters(),
        objective=lambda trajectory, params: (
            params.B0 if not trajectory else trajectory[-1].next_backlog
        ),
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
        objective=lambda trajectory, params: (
            params.B0 if not trajectory else trajectory[-1].next_backlog
        ),
        direction="max",
    )

    assert result.best_remediation_fraction == 0.0
    assert len(result.evaluations) == 1
    assert result.evaluations[0].remediation_fraction == 0.0
