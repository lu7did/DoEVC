"""Core model parameter entities for the DoEVC s001 sequence."""

from dataclasses import dataclass


def ensure_non_negative(name: str, value: float) -> None:
    """Ensure that a numeric value is not negative."""
    if value < 0:
        raise ValueError(f"{name} must be non-negative.")


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
        """Validate the parameter set after initialization."""
        ensure_non_negative("B0", self.B0)
        ensure_non_negative("D0", self.D0)
        ensure_non_negative("V0", self.V0)
        ensure_non_negative("alpha", self.alpha)
        ensure_non_negative("beta", self.beta)
        ensure_non_negative("gamma", self.gamma)
        ensure_non_negative("theta", self.theta)
        ensure_non_negative("lambda_", self.lambda_)
        ensure_non_negative("rho", self.rho)
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
