"""Tests for deterministic simulation visualizations."""

from dataclasses import replace
from pathlib import Path

from s004 import (
    DebtFirstPolicy,
    plot_optimal_u_distribution,
    plot_sensitivity_heatmap,
    plot_simulation,
    run_monte_carlo,
    simulate_deterministic_sprints,
)
from tests.support import create_competing_parameters, create_parameters


def test_plot_simulation_writes_non_empty_png(tmp_path: Path) -> None:
    """Render a trajectory without requiring an interactive display."""
    states = simulate_deterministic_sprints(
        replace(create_competing_parameters(), D0=4.0, K=2),
        0.5,
    )
    filepath = tmp_path / "simulation.png"

    plot_simulation(states, filepath)

    assert filepath.is_file()
    assert filepath.stat().st_size > 0


def test_plot_sensitivity_heatmap_writes_sized_png(tmp_path: Path) -> None:
    """Render one mean remediation value for every parameter combination."""
    filepath = tmp_path / "sensitivity.png"

    matrix = plot_sensitivity_heatmap(
        ("gamma", (0.0, 0.05)),
        ("theta", (0.0, 0.5, 0.9)),
        create_parameters(),
        DebtFirstPolicy(),
        filepath,
    )

    assert len(matrix) == 3
    assert all(len(row) == 2 for row in matrix)
    assert filepath.is_file()
    assert filepath.stat().st_size > 0


def test_plot_optimal_u_distribution_writes_non_empty_png(tmp_path: Path) -> None:
    """Render a boxplot from the metrics produced by Monte Carlo."""
    simulation = run_monte_carlo(
        3,
        DebtFirstPolicy(),
        seed=1,
        base_parameters=create_parameters(),
    )
    filepath = tmp_path / "optimal-u-distribution.png"

    plot_optimal_u_distribution(simulation, filepath)

    assert filepath.is_file()
    assert filepath.stat().st_size > 0
