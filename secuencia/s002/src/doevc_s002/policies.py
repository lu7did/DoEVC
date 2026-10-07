"""Remediation policies for deterministic simulations."""

from numbers import Real


class DebtFirstPolicy:
    """Allocate all capacity to technical debt until it is eliminated."""

    def decide_u(self, backlog: Real, debt: Real) -> float:
        """Return the remediation fraction for the current technical debt."""
        _validate_work("backlog", backlog)
        _validate_work("debt", debt)
        return 1.0 if debt > 0 else 0.0


class BacklogFirstPolicy:
    """Allocate all capacity to backlog until it is eliminated."""

    def decide_u(self, backlog: Real, debt: Real) -> float:
        """Return the remediation fraction for backlog-first delivery."""
        _validate_work("backlog", backlog)
        _validate_work("debt", debt)
        return 0.0 if backlog > 0 else 1.0 if debt > 0 else 0.0


def _validate_work(name: str, value: Real) -> None:
    """Validate a non-negative backlog or debt quantity."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number.")
    if value < 0:
        raise ValueError(f"{name} must be non-negative.")
