"""Tests for simulation visualizations."""

import pytest

from doevc_s001 import (
    DebtFirstPolicy,
    ModelParameters,
    plot_optimal_u_distribution,
    plot_sensitivity_heatmap,
    plot_simulation,
    run_monte_carlo,
    simulate_deterministic_sprints,
)


def test_plot_simulation_writes_a_non_empty_png(tmp_path) -> None:
    """Render a deterministic trajectory without requiring a display."""
    states = simulate_deterministic_sprints(_parameters(), 0.5)
    filepath = tmp_path / "simulation.png"

    plot_simulation(states, filepath)

    assert filepath.is_file()
    assert filepath.stat().st_size > 0


def test_plot_optimal_u_distribution_writes_a_non_empty_png(tmp_path) -> None:
    """Render a boxplot from Monte Carlo metrics without a display."""
    simulation = run_monte_carlo(
        3,
        DebtFirstPolicy(),
        seed=1,
        base_parameters=_parameters(),
    )
    filepath = tmp_path / "optimal-u-distribution.png"

    plot_optimal_u_distribution(simulation, filepath)

    assert filepath.is_file()
    assert filepath.stat().st_size > 0


def test_plot_optimal_u_distribution_accepts_individual_results(tmp_path) -> None:
    """Render a boxplot from the individual metrics produced by C3."""
    simulation = run_monte_carlo(
        2,
        DebtFirstPolicy(),
        seed=1,
        base_parameters=_parameters(),
    )
    filepath = tmp_path / "individual-optimal-u-distribution.png"

    plot_optimal_u_distribution(
        tuple(run.metrics for run in simulation.runs),
        filepath,
    )

    assert filepath.is_file()
    assert filepath.stat().st_size > 0


def test_plot_sensitivity_heatmap_writes_a_matrix_sized_png(tmp_path) -> None:
    """Render one mean remediation value for every parameter combination."""
    filepath = tmp_path / "sensitivity.png"

    matrix = plot_sensitivity_heatmap(
        ("gamma", (0.0, 0.05)),
        ("theta", (0.0, 0.5, 0.9)),
        _parameters(),
        DebtFirstPolicy(),
        filepath,
    )

    assert len(matrix) == 3
    assert all(len(row) == 2 for row in matrix)
    assert filepath.is_file()
    assert filepath.stat().st_size > 0


@pytest.mark.parametrize(
    ("param1_name", "param2_name"),
    (
        ("B0", "D0"),
        ("V0", "alpha"),
        ("beta", "lambda_"),
        ("rho", "s"),
    ),
)
def test_plot_sensitivity_heatmap_supports_all_continuous_parameters(
    tmp_path,
    param1_name: str,
    param2_name: str,
) -> None:
    """Allow every continuous ModelParameters field to be selected."""
    filepath = tmp_path / f"{param1_name}-{param2_name}.png"

    matrix = plot_sensitivity_heatmap(
        (param1_name, (0.1,)),
        (param2_name, (0.2,)),
        _parameters(),
        DebtFirstPolicy(),
        filepath,
    )

    assert len(matrix) == 1
    assert len(matrix[0]) == 1
    assert 0.0 <= matrix[0][0] <= 1.0
    assert filepath.is_file()


def _parameters() -> ModelParameters:
    """Return a compact deterministic trajectory for visualization."""
    return ModelParameters(
        B0=10.0,
        D0=4.0,
        V0=10.0,
        alpha=0.0,
        beta=0.0,
        gamma=0.0,
        theta=0.0,
        lambda_=0.0,
        rho=0.0,
        K=2,
        s=1.0,
    )
