"""Non-interactive visualizations for deterministic simulations."""

# pyright: reportUnknownMemberType=false

from collections.abc import Sequence
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from .sprint import SprintState


def plot_simulation(states: Sequence[SprintState], filepath: str | Path) -> None:
    """Render backlog and technical debt by sprint to a PNG file."""
    sprints = range(1, len(states) + 1)
    figure, axis = plt.subplots()
    axis.plot(sprints, tuple(state.backlog for state in states), label="B_k")
    axis.plot(sprints, tuple(state.technical_debt for state in states), label="D_k")
    axis.set_xlabel("Sprint")
    axis.set_ylabel("Work")
    axis.legend()
    figure.tight_layout()
    figure.savefig(filepath, format="png")
    plt.close(figure)
