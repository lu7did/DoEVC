"""Version metadata for the DoEVC s001 sequence."""

VERSION = "1.0"
BUILD = "021"
SEQUENCE_ID = "s001"
PYTHON_VERSION = "3.13"


def get_version_label() -> str:
    """Return the human-readable version label for s001."""
    return f"{VERSION} build {BUILD}"
