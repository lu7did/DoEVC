"""Policy abstractions and baseline implementations for DoEVC s001."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .models import ModelParameters
from .sprint import SprintState


@runtime_checkable
class Policy(Protocol):
    """Define the common interface for remediation decision policies."""

    def decide_u(self, state: SprintState, params: ModelParameters) -> float:
        """Return the remediation fraction for the current sprint."""


class DebtFirstPolicy:
    """Use full remediation while any technical debt remains."""

    def decide_u(self, state: SprintState, params: ModelParameters) -> float:
        """Choose the remediation fraction for the current sprint."""
        del params
        return 1.0 if state.technical_debt > 0 else 0.0
