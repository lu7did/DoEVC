"""Visualization helpers for deterministic and Monte Carlo DoEVC outputs."""

from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import Protocol, cast

import matplotlib

matplotlib.use("Agg")

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from .montecarlo import MonteCarloRunResult
from .sprint import SprintState


class _Axes(Protocol):
    """Protocol covering the axes methods used by the plotting helpers."""

    def plot(
        self,
        x: tuple[int, ...],
        y: tuple[float, ...],
        *,
        label: str,
        linewidth: int,
    ) -> object: ...

    def set_xlabel(self, xlabel: str) -> object: ...

    def set_ylabel(self, ylabel: str) -> object: ...

    def set_title(self, title: str) -> object: ...

    def legend(self) -> object: ...

    def grid(self, visible: bool, *, alpha: float) -> None: ...

    def boxplot(self, x: tuple[float, ...]) -> object: ...


class _FigureSaver(Protocol):
    """Protocol covering the figure save method used by the plot helper."""

    def savefig(self, fname: str | PathLike[str], *, format: str) -> None: ...


def plot_simulation(
    states: tuple[SprintState, ...],
    destination: str | PathLike[str],
) -> Path:
    """Render backlog and technical debt trajectories as a PNG chart."""
    destination_path = Path(destination)
    sprint_indices = tuple(range(1, len(states) + 1))
    backlog_values = tuple(state.backlog for state in states)
    debt_values = tuple(state.technical_debt for state in states)

    figure = Figure(figsize=(8, 4.5), tight_layout=True)
    FigureCanvasAgg(figure)
    axes = cast(_Axes, figure.subplots())
    axes.plot(sprint_indices, backlog_values, label="B_k", linewidth=2)
    axes.plot(sprint_indices, debt_values, label="D_k", linewidth=2)
    axes.set_xlabel("Sprint")
    axes.set_ylabel("Trabajo pendiente")
    axes.set_title("Evolucion de backlog y deuda tecnica")
    axes.legend()
    axes.grid(True, alpha=0.3)
    cast(_FigureSaver, figure).savefig(destination_path, format="png")
    return destination_path


def plot_optimal_u_distribution(
    results: tuple[MonteCarloRunResult, ...],
    destination: str | PathLike[str],
) -> Path:
    """Render a PNG boxplot for the per-run optimal remediation distribution."""
    destination_path = Path(destination)
    remediation_values = tuple(run.average_remediation_fraction for run in results)
    if not remediation_values:
        raise ValueError("results must not be empty.")

    figure = Figure(figsize=(6, 4.5), tight_layout=True)
    FigureCanvasAgg(figure)
    axes = cast(_Axes, figure.subplots())
    axes.boxplot(remediation_values)
    axes.set_ylabel("u_k promedio")
    axes.set_title("Distribucion de u_k optimo")
    axes.grid(True, alpha=0.3)
    cast(_FigureSaver, figure).savefig(destination_path, format="png")
    return destination_path
