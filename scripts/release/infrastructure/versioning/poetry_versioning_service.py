from scripts.release.application.ports.outbound import VersioningService
from scripts.release.infrastructure.commons.process import run
from scripts.release.domain.value_objects import (
    ReleaseLevel,
    ReleaseVersion,
)


class PoetryVersioningService(VersioningService):
    def compute_next_version(
        self,
        level: ReleaseLevel,
    ) -> ReleaseVersion:
        raw_version = run(["poetry", "version"])
        current_version = self._parse_poetry_version_output(raw_version)

        raw_version = current_version.value

        major, minor, patch = map(int, raw_version.split("."))

        if level.value == "major":
            return ReleaseVersion(major + 1, 0, 0)

        if level.value == "minor":
            return ReleaseVersion(major, minor + 1, 0)

        return ReleaseVersion(major, minor, patch + 1)

    def apply_version(
        self,
        version: ReleaseVersion,
    ) -> None:
        run(["poetry", "version", version.value])

    def rollback_version(
        self,
        previous: ReleaseVersion,
    ) -> None:
        run(["poetry", "version", previous.value])

    def _parse_poetry_version_output(self, raw_current_version: str) -> ReleaseVersion:
        _, raw_version = raw_current_version.split()
        major, minor, patch = map(int, raw_version.split("."))

        return ReleaseVersion(major, minor, patch)
