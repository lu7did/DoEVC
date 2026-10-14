"""Regression tests for generated simulation charts."""

from doevc_s002 import (
    DebtFirstPolicy,
    ModelParameters,
    plot_optimal_u_distribution,
    plot_sensitivity_heatmap,
    plot_simulation,
    run_monte_carlo,
    simulate_deterministic_sprints,
)


def test_plot_simulation_creates_a_nonempty_png(tmp_path: object) -> None:
    """Save the sprint trajectory as a PNG without an interactive display."""
    filepath = tmp_path / "simulation.png"  # type: ignore[operator]
    states = simulate_deterministic_sprints(
        ModelParameters(10, 5, 5, 0, 0, 0, 0, 0, 0, 2), 0.5
    )

    plot_simulation(states, filepath)

    assert filepath.exists()
    assert filepath.stat().st_size > 0


def test_plot_sensitivity_heatmap_creates_png_and_expected_matrix(
    tmp_path: object,
) -> None:
    """Return one mean-remediation value for each parameter combination."""
    filepath = tmp_path / "heatmap.png"  # type: ignore[operator]
    matrix = plot_sensitivity_heatmap(
        ("gamma", [0.0, 0.1]),
        ("alpha", [0.0, 0.2, 0.4]),
        ModelParameters(10, 5, 5, 0, 0, 0, 0, 0, 0, 2),
        DebtFirstPolicy(),
        filepath,
    )

    assert len(matrix) == 3
    assert all(len(row) == 2 for row in matrix)
    assert filepath.exists()
    assert filepath.stat().st_size > 0


def test_plot_optimal_u_distribution_creates_a_nonempty_png(tmp_path: object) -> None:
    """Save a boxplot from Monte Carlo remediation metrics."""
    filepath = tmp_path / "distribution.png"  # type: ignore[operator]

    plot_optimal_u_distribution(run_monte_carlo(2, DebtFirstPolicy(), 7), filepath)

    assert filepath.exists()
    assert filepath.stat().st_size > 0
