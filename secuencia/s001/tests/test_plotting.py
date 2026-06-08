"""Tests for deterministic and Monte Carlo plotting helpers in DoEVC s001."""

import pytest

from doevc_s001 import (
    DebtFirstPolicy,
    EconomicObjectiveFunction,
    ModelParameters,
    OptimalLocalPolicy,
    plot_optimal_u_distribution,
    plot_simulation,
    run_monte_carlo,
    simulate_deterministic_sprints,
)


def sample_parameters() -> ModelParameters:
    """Return a representative parameter set for plotting tests."""
    return ModelParameters(
        B0=8.0,
        D0=4.0,
        V0=4.0,
        alpha=0.0,
        beta=0.2,
        gamma=0.01,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=3,
        s=1.0,
    )


def test_plot_simulation_creates_a_non_empty_png(tmp_path: str) -> None:
    """Create a PNG file for a deterministic sprint trajectory."""
    states = simulate_deterministic_sprints(sample_parameters(), DebtFirstPolicy())

    png_path = plot_simulation(states, tmp_path / "simulation.png")

    assert png_path.exists()
    assert png_path.suffix == ".png"
    assert png_path.stat().st_size > 0
    assert png_path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")


def test_plot_optimal_u_distribution_creates_a_non_empty_png(tmp_path: str) -> None:
    """Create a PNG boxplot from valid Monte Carlo run results."""
    result = run_monte_carlo(
        4,
        OptimalLocalPolicy(objective=EconomicObjectiveFunction()),
        seed=321,
        base_parameters=sample_parameters(),
    )

    png_path = plot_optimal_u_distribution(
        result.runs,
        tmp_path / "optimal-u-distribution.png",
    )

    assert png_path.exists()
    assert png_path.suffix == ".png"
    assert png_path.stat().st_size > 0
    assert png_path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")


def test_plot_optimal_u_distribution_rejects_empty_results(tmp_path: str) -> None:
    """Reject boxplot generation without any Monte Carlo runs."""
    with pytest.raises(ValueError, match="results must not be empty"):
        plot_optimal_u_distribution((), tmp_path / "empty-optimal-u.png")
