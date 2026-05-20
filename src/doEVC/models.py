"""Core model entities for the DoEVC project."""

from dataclasses import dataclass


def _ensure_non_negative(name: str, value: float | int) -> None:
    """Ensure that a numeric value is not negative."""
    if value < 0:
        raise ValueError(f"{name} must be non-negative.")


def _ensure_unit_interval(name: str, value: float) -> None:
    """Ensure that a numeric value belongs to the inclusive unit interval."""
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0.")


@dataclass(slots=True, frozen=True)
class ModelParameters:
    """Store the validated base parameters of the deterministic model."""

    B0: float
    D0: float
    V0: float
    alpha: float
    beta: float
    gamma: float
    theta: float
    lambda_: float
    rho: float
    K: int

    def __post_init__(self) -> None:
        """Validate model parameters immediately after initialization."""
        _ensure_non_negative("B0", self.B0)
        _ensure_non_negative("D0", self.D0)
        _ensure_non_negative("V0", self.V0)
        _ensure_non_negative("gamma", self.gamma)
        _ensure_non_negative("theta", self.theta)
        _ensure_non_negative("lambda_", self.lambda_)
        _ensure_non_negative("rho", self.rho)
        _ensure_unit_interval("alpha", self.alpha)
        _ensure_unit_interval("beta", self.beta)
        if self.K <= 0:
            raise ValueError("K must be greater than zero.")

    def to_dict(self) -> dict[str, float | int]:
        """Serialize the parameter set to a dictionary."""
        return {
            "B0": self.B0,
            "D0": self.D0,
            "V0": self.V0,
            "alpha": self.alpha,
            "beta": self.beta,
            "gamma": self.gamma,
            "theta": self.theta,
            "lambda_": self.lambda_,
            "rho": self.rho,
            "K": self.K,
        }
