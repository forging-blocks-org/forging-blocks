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
        output = run(["poetry", "version"])
        _, raw_version = output.split()

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
