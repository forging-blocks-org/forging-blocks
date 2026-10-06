"""Tests for release version validation."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

VALIDATOR = Path(__file__).parents[2] / "scripts/pipeline/validate_release_version.sh"


def run_validator(release_version: str | None) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    if release_version is None:
        environment.pop("RELEASE_VERSION", None)
    else:
        environment["RELEASE_VERSION"] = release_version

    return subprocess.run(
        ["bash", str(VALIDATOR)],
        capture_output=True,
        check=False,
        env=environment,
        text=True,
    )


@pytest.mark.unit
class TestValidateReleaseVersion:
    @pytest.mark.parametrize("release_version", ["0.0.0", "1.2.3", "10.20.30"])
    def test_when_version_is_normalized_semver_then_succeeds(
        self,
        release_version: str,
    ) -> None:
        result = run_validator(release_version)

        assert result.returncode == 0
        assert f"Release version validated: {release_version}" in result.stdout

    @pytest.mark.parametrize(
        "release_version",
        ["v1.2.3", "1.2", "1.2.3.4", "01.2.3", "1.2.3-alpha", "1.2.3+build"],
    )
    def test_when_version_is_not_normalized_semver_then_fails(
        self,
        release_version: str,
    ) -> None:
        result = run_validator(release_version)

        assert result.returncode != 0
        assert "normalized SemVer" in result.stderr

    def test_when_version_is_missing_then_fails(self) -> None:
        result = run_validator(None)

        assert result.returncode != 0
        assert "RELEASE_VERSION" in result.stderr
