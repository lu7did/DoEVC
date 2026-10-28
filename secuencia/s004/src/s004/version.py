"""Version metadata for S004."""

VERSION = "1.0"
BUILD = "000"


def display_version() -> str:
    """Return the user-facing package version."""
    return f"{VERSION} build {BUILD}"
