"""Interchangeable allocation policies for deterministic simulations."""

from typing import Protocol, runtime_checkable

from .models import ModelParameters
from .sprint import SprintState


@runtime_checkable
class Policy(Protocol):  # pylint: disable=too-few-public-methods
    """Select the remediation fraction for the current simulation state."""

    def decide_u(self, state: SprintState, params: ModelParameters) -> float:
        """Return a remediation allocation in the closed interval [0, 1]."""
        ...


class DebtFirstPolicy:  # pylint: disable=too-few-public-methods
    """Allocate all capacity to remediation while technical debt remains."""

    def decide_u(self, state: SprintState, params: ModelParameters) -> float:
        """Select remediation when the current state has technical debt."""
        del params
        return 1.0 if state.debt > 0 else 0.0


class BacklogFirstPolicy:  # pylint: disable=too-few-public-methods
    """Allocate capacity to delivery until functional backlog is cleared."""

    def decide_u(self, state: SprintState, params: ModelParameters) -> float:
        """Select delivery while backlog remains, then remediation for debt."""
        del params
        if state.backlog > 0:
            return 0.0
        return 1.0 if state.debt > 0 else 0.0


class ProportionalPolicy:  # pylint: disable=too-few-public-methods
    """Allocate remediation capacity according to the relative debt level."""

    def decide_u(self, state: SprintState, params: ModelParameters) -> float:
        """Select the debt fraction of the current total work."""
        del params
        total_work = state.backlog + state.debt
        return state.debt / total_work if total_work > 0 else 0.0
