"""Validated parameter structures for reproducible simulations."""

from dataclasses import asdict, dataclass
from numbers import Real


def _require_non_negative(name: str, value: object) -> None:
    """Validate that a model parameter is a non-negative real number."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number.")
    if value < 0:
        raise ValueError(f"{name} must not be negative.")


def _require_positive(name: str, value: object) -> None:
    """Validate that a model parameter is a strictly positive real number."""
    _require_non_negative(name, value)
    if value == 0:
        raise ValueError(f"{name} must be greater than zero.")


@dataclass(frozen=True, slots=True)
class ModelParameters:  # pylint: disable=too-many-instance-attributes
    """Immutable inputs used to reproduce model simulations."""

    B0: float  # pylint: disable=invalid-name
    D0: float  # pylint: disable=invalid-name
    V0: float  # pylint: disable=invalid-name
    alpha: float
    beta: float
    gamma: float
    theta: float
    lambda_: float
    rho: float
    K: int  # pylint: disable=invalid-name
    s: float = 1.0

    def __post_init__(self) -> None:
        """Reject invalid parameter values after initialization."""
        for field_name in (
            "B0",
            "D0",
            "alpha",
            "beta",
            "gamma",
            "theta",
            "lambda_",
            "rho",
            "s",
        ):
            _require_non_negative(field_name, getattr(self, field_name))
        _require_positive("V0", self.V0)

        if isinstance(self.K, bool) or not isinstance(self.K, int):
            raise TypeError("K must be an integer.")
        if self.K < 0:
            raise ValueError("K must not be negative.")

    def to_dict(self) -> dict[str, float | int]:
        """Return a serialization-friendly representation of the parameters."""
        return asdict(self)
