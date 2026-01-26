from scripts.release.application.ports.outbound import VersioningService
from scripts.release.infrastructure.commons.process import CommandRunner, SubprocessCommandRunner
from scripts.release.domain.value_objects import (
    ReleaseLevel,
    ReleaseVersion,
)


class PoetryVersioningService(VersioningService):
    def __init__(self, runner: CommandRunner = SubprocessCommandRunner()) -> None:
        self._runner = runner

    def current_version(self) -> ReleaseVersion:
        return self._poetry_version()

    def compute_next_version(
        self,
        level: ReleaseLevel,
    ) -> ReleaseVersion:
        current_version = self._poetry_version()

        major, minor, patch = map(int, current_version.value.split("."))
        if level.value == "major":
            return ReleaseVersion(major + 1, 0, 0)

        if level.value == "minor":
            return ReleaseVersion(major, minor + 1, 0)

        return ReleaseVersion(major, minor, patch + 1)

    def apply_version(
        self,
        version: ReleaseVersion,
    ) -> None:
        self._runner.run(["poetry", "version", version.value])

    def rollback_version(
        self,
        previous: ReleaseVersion,
    ) -> None:
        self._runner.run(["poetry", "version", previous.value])

    def _poetry_version(self) -> ReleaseVersion:
        raw_current_version = self._runner.run(["poetry", "version"])

        _, raw_version = raw_current_version.split()
        major, minor, patch = map(int, raw_version.split("."))

        return ReleaseVersion(major, minor, patch)
