"""Version metadata for DoEVC."""

VERSION = "1.0"
BUILD = "001"
__version__ = "1.0.0"


def get_version_label() -> str:
    """Return the human-readable project version label."""
    return f"{VERSION} build {BUILD}"
