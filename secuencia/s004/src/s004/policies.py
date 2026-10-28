"""Remediation decision policies."""

from typing import Protocol, runtime_checkable

from .models import ModelParameters
from .sprint import SprintState


@runtime_checkable
class Policy(Protocol):  # pylint: disable=too-few-public-methods
    """Define the interface used by sprint simulation policies."""

    def decide_u(self, state: SprintState, parameters: ModelParameters) -> float:
        """Return the remediation fraction for the current sprint."""
        ...


class DebtFirstPolicy:  # pylint: disable=too-few-public-methods
    """Allocate all capacity to debt remediation while debt remains."""

    def decide_u(self, state: SprintState, parameters: ModelParameters) -> float:
        """Return full remediation if technical debt exists, otherwise none."""
        del parameters
        return 1.0 if state.technical_debt > 0 else 0.0


class BacklogFirstPolicy:  # pylint: disable=too-few-public-methods
    """Allocate capacity to backlog work before debt remediation."""

    def decide_u(self, state: SprintState, parameters: ModelParameters) -> float:
        """Return remediation only after the functional backlog is complete."""
        del parameters
        if state.backlog > 0:
            return 0.0
        return 1.0 if state.technical_debt > 0 else 0.0
