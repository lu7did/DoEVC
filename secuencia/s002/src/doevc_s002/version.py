"""Version metadata for the second sequence."""

VERSION = "1.0"
BUILD = "010"
SEQUENCE_ID = "s002"
PYTHON_VERSION = "3.13"


def get_version_label() -> str:
    """Return the human-readable release label."""
    return f"{VERSION} build {BUILD}"
