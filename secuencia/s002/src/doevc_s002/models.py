"""Validated model parameter structures."""

from dataclasses import asdict, dataclass
from numbers import Real


def _validate_non_negative(name: str, value: Real) -> None:
    """Ensure a model quantity is a non-negative real number."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number.")
    if value < 0:
        raise ValueError(f"{name} must be non-negative.")


@dataclass(frozen=True, slots=True)
class ModelParameters:
    """Immutable input parameters for reproducible model simulations."""

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
    s: float = 1.0

    def __post_init__(self) -> None:
        """Validate every parameter after initialization."""
        for name in (
            "B0",
            "D0",
            "V0",
            "alpha",
            "beta",
            "gamma",
            "theta",
            "lambda_",
            "rho",
            "s",
        ):
            _validate_non_negative(name, getattr(self, name))

        if isinstance(self.K, bool) or not isinstance(self.K, int):
            raise TypeError("K must be an integer.")
        if self.K < 0:
            raise ValueError("K must be non-negative.")

    def to_dict(self) -> dict[str, float | int]:
        """Return a serializable representation of the parameters."""
        return asdict(self)
