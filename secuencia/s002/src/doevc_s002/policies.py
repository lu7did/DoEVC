"""Remediation policies for deterministic simulations."""

from numbers import Real


class DebtFirstPolicy:
    """Allocate all capacity to technical debt until it is eliminated."""

    def decide_u(self, debt: Real) -> float:
        """Return the remediation fraction for the current technical debt."""
        if isinstance(debt, bool) or not isinstance(debt, Real):
            raise TypeError("debt must be a real number.")
        if debt < 0:
            raise ValueError("debt must be non-negative.")
        return 1.0 if debt > 0 else 0.0
