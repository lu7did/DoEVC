"""Non-interactive visualizations for deterministic simulations."""

from collections.abc import Iterable
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

from matplotlib import pyplot as plt

from .sprint import SprintState


def plot_simulation(states: Iterable[SprintState], filepath: str | Path) -> None:
    """Save backlog and debt values across sprint indices as a PNG."""
    trajectory = list(states)
    sprints = range(1, len(trajectory) + 1)
    figure, axis = plt.subplots()
    axis.plot(sprints, [state.backlog for state in trajectory], label="Backlog")
    axis.plot(sprints, [state.debt for state in trajectory], label="Technical debt")
    axis.set_xlabel("Sprint")
    axis.set_ylabel("Work")
    axis.legend()
    figure.tight_layout()
    figure.savefig(filepath, format="png")
    plt.close(figure)
