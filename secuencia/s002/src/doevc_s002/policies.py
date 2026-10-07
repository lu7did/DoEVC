"""Remediation policies for deterministic simulations."""

from numbers import Real
from typing import Protocol

from .models import ModelParameters
from .sprint import SprintState


class Policy(Protocol):
    """Contract for remediation policies accepted by the simulator."""

    def decide_u(self, state: SprintState, params: ModelParameters) -> float:
        """Choose a remediation fraction for the current sprint."""


class DebtFirstPolicy:
    """Allocate all capacity to technical debt until it is eliminated."""

    def decide_u(self, state: SprintState, params: ModelParameters) -> float:
        """Return the remediation fraction for the current technical debt."""
        _validate_work("backlog", state.backlog)
        _validate_work("debt", state.debt)
        return 1.0 if state.debt > 0 else 0.0


class BacklogFirstPolicy:
    """Allocate all capacity to backlog until it is eliminated."""

    def decide_u(self, state: SprintState, params: ModelParameters) -> float:
        """Return the remediation fraction for backlog-first delivery."""
        _validate_work("backlog", state.backlog)
        _validate_work("debt", state.debt)
        return 0.0 if state.backlog > 0 else 1.0 if state.debt > 0 else 0.0


class ProportionalPolicy:
    """Allocate capacity in proportion to the current technical debt."""

    def decide_u(self, state: SprintState, params: ModelParameters) -> float:
        """Return debt as a fraction of all remaining work."""
        _validate_work("backlog", state.backlog)
        _validate_work("debt", state.debt)
        total_work = state.backlog + state.debt
        return 0.0 if total_work == 0 else float(state.debt / total_work)


def _validate_work(name: str, value: Real) -> None:
    """Validate a non-negative backlog or debt quantity."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number.")
    if value < 0:
        raise ValueError(f"{name} must be non-negative.")
