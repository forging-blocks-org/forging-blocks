"""Tests for the published package surface."""

import tomllib
from pathlib import Path
from typing import cast

import pytest

PROJECT_FILE = Path(__file__).parents[2] / "pyproject.toml"


@pytest.mark.unit
class TestPackageMetadata:
    def test_project_does_not_publish_console_entry_points(self) -> None:
        project = tomllib.loads(PROJECT_FILE.read_text())
        project_metadata = cast(dict[str, object], project["project"])
        scripts = cast(dict[str, str], project_metadata.get("scripts", {}))

        assert scripts == {}
