"""Policy abstractions and baseline implementations for DoEVC s001."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from .models import ModelParameters
from .sprint import SprintState


@runtime_checkable
class Policy(Protocol):
    """Define the common interface for remediation decision policies."""

    def decide_u(self, state: SprintState, params: ModelParameters) -> float:
        """Return the remediation fraction for the current sprint."""
        ...


@dataclass(slots=True, frozen=True)
class DebtFirstPolicy:
    """Use full remediation while any technical debt remains."""

    def decide_u(self, state: SprintState, params: ModelParameters) -> float:
        """Choose the remediation fraction for the current sprint."""
        del params
        return 1.0 if state.technical_debt > 0 else 0.0


@dataclass(slots=True, frozen=True)
class BacklogFirstPolicy:
    """Spend full capacity on backlog until it reaches zero."""

    def decide_u(self, state: SprintState, params: ModelParameters) -> float:
        """Choose the remediation fraction for the current sprint."""
        del params
        if state.backlog > 0:
            return 0.0
        return 1.0 if state.technical_debt > 0 else 0.0


@dataclass(slots=True, frozen=True)
class ProportionalDebtPolicy:
    """Split capacity proportionally to the current relative debt load."""

    def decide_u(self, state: SprintState, params: ModelParameters) -> float:
        """Choose the remediation fraction for the current sprint."""
        del params
        total_work = state.backlog + state.technical_debt
        if total_work == 0:
            return 0.0
        return state.technical_debt / total_work
