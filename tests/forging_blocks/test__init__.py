"""Tests for the forging_blocks package root."""

import re

import pytest

from forging_blocks import __version__


@pytest.mark.unit
class TestInit:
    def test_version_is_non_empty_string(self) -> None:
        """__version__ must be a non-empty string."""
        assert isinstance(__version__, str)
        assert len(__version__) > 0

    def test_version_follows_pep440_format(self) -> None:
        """__version__ must match PEP 440 (major.minor[.patch])."""
        assert re.match(r"^\d+\.\d+(?:\.\d+)?", __version__), (
            f"Version '{__version__}' does not match PEP 440 format"
        )

    def test_version_resolves_from_package_metadata(self) -> None:
        """__version__ must resolve from package metadata, not the fallback."""
        assert __version__ != "0.0.0-dev", f"Expected package version, got fallback '{__version__}'"

    def test_version_fallback_when_package_not_found(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """When PackageNotFoundError is raised, __version__ must be '0.0.0-dev'."""
        import importlib
        import importlib.metadata
        from importlib.metadata import PackageNotFoundError

        import forging_blocks

        def _raise_not_found(_name: str) -> str:
            raise PackageNotFoundError

        monkeypatch.setattr(importlib.metadata, "version", _raise_not_found)

        try:
            importlib.reload(forging_blocks)
            assert forging_blocks.__version__ == "0.0.0-dev"
        finally:
            monkeypatch.undo()
            importlib.reload(forging_blocks)
