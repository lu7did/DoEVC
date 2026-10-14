"""Regression tests for generated simulation charts."""

from doevc_s002 import ModelParameters, plot_simulation, simulate_deterministic_sprints


def test_plot_simulation_creates_a_nonempty_png(tmp_path: object) -> None:
    """Save the sprint trajectory as a PNG without an interactive display."""
    filepath = tmp_path / "simulation.png"  # type: ignore[operator]
    states = simulate_deterministic_sprints(
        ModelParameters(10, 5, 5, 0, 0, 0, 0, 0, 0, 2), 0.5
    )

    plot_simulation(states, filepath)

    assert filepath.exists()
    assert filepath.stat().st_size > 0
