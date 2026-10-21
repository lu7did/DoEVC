"""Validated parameter structures for s003."""

from dataclasses import asdict, dataclass
from numbers import Real


def _require_non_negative(name: str, value: object) -> None:
    """Validate a non-negative numeric model parameter."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number.")
    if value < 0:
        raise ValueError(f"{name} must not be negative.")


@dataclass(frozen=True, slots=True)
class ModelParameters:  # pylint: disable=too-many-instance-attributes
    """Immutable inputs used to reproduce model experiments."""

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

    def __post_init__(self) -> None:
        """Reject invalid values after dataclass initialization."""
        for field_name in (
            "B0",
            "D0",
            "V0",
            "alpha",
            "beta",
            "gamma",
            "theta",
            "lambda_",
            "rho",
        ):
            _require_non_negative(field_name, getattr(self, field_name))
        if self.K < 0:
            raise ValueError("K must not be negative.")

    def to_dict(self) -> dict[str, float | int]:
        """Return a serialization-friendly parameter mapping."""
        return asdict(self)
