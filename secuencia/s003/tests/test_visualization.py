"""Regression tests for deterministic simulation visualizations."""

from pathlib import Path

from doevc_s003 import (
    ModelParameters,
    ProportionalPolicy,
    RunMetrics,
    SprintState,
    plot_optimal_u_distribution,
    plot_sensitivity_heatmap,
    plot_simulation,
)


def test_simulation_plot_creates_a_non_empty_png(tmp_path: Path) -> None:
    """Write the backlog and debt trajectory to a portable PNG file."""
    path = tmp_path / "simulation.png"
    states = [
        SprintState(10, 5, 0.2, 8, 1.6, 6.4, 3.6, 3.4),
        SprintState(3.6, 3.4, 0.2, 8, 1.6, 6.4, 0, 1.8),
    ]

    plot_simulation(states, path)

    assert path.is_file()
    assert path.stat().st_size > 0


def test_sensitivity_heatmap_creates_png_with_expected_matrix_dimensions(
    tmp_path: Path,
) -> None:
    """Produce one average-allocation value for each parameter combination."""
    path = tmp_path / "sensitivity.png"
    parameters = ModelParameters(10, 5, 10, 0, 0, 0, 0, 0, 0, 1)

    matrix = plot_sensitivity_heatmap(
        ("B0", [10, 20]),
        ("D0", [5, 15, 25]),
        parameters,
        ProportionalPolicy(),
        path,
    )

    assert len(matrix) == 3
    assert all(len(row) == 2 for row in matrix)
    assert path.is_file()
    assert path.stat().st_size > 0


def test_optimal_allocation_boxplot_creates_a_non_empty_png(tmp_path: Path) -> None:
    """Write a PNG boxplot from the per-run C3 allocation metrics."""
    path = tmp_path / "allocation-distribution.png"
    metrics = [
        RunMetrics(2, 3, 0.2, 4),
        RunMetrics(2, 2, 0.5, 3),
        RunMetrics(2, 1, 0.8, 2),
    ]

    plot_optimal_u_distribution(metrics, path)

    assert path.is_file()
    assert path.stat().st_size > 0
