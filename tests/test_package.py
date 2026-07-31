"""Smoke tests for the package foundation."""

import tsmeta


def test_package_can_be_imported() -> None:
    """Verify that the installed package is importable."""
    assert tsmeta.__name__ == "tsmeta"


def test_package_exposes_version() -> None:
    """Expose package version metadata."""
    assert tsmeta.__version__ == "0.1.0"
