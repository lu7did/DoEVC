"""Tests for simulation visualizations."""

from doevc_s001 import (
    DebtFirstPolicy,
    ModelParameters,
    plot_optimal_u_distribution,
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
