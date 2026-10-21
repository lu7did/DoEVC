"""Regression tests for deterministic simulation visualizations."""

from pathlib import Path

from doevc_s003 import SprintState, plot_simulation


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
