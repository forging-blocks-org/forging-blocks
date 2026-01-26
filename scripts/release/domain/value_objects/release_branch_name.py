from typing import Hashable
from forging_blocks.domain import ValueObject

from scripts.release.domain.value_objects.release_version import ReleaseVersion
from scripts.release.domain.errors import InvalidReleaseVersionError, InvalidReleaseBranchNameError


class ReleaseBranchName(ValueObject[str]):
    __slots__ = ("_value",)

    PREFIX = "release/v"

    def __init__(self, value: str) -> None:
        super().__init__()

        if not value.startswith(self.PREFIX):
            raise InvalidReleaseBranchNameError(value)

        version_part = value[len(self.PREFIX) :]
        parts = version_part.split(".")

        if len(parts) != 3:
            raise InvalidReleaseBranchNameError(value)

        try:
            major, minor, patch = (int(p) for p in parts)
        except ValueError as exc:
            raise InvalidReleaseBranchNameError(value) from exc

        try:
            ReleaseVersion(major, minor, patch)
        except InvalidReleaseVersionError as exc:
            raise InvalidReleaseBranchNameError(value) from exc

        self._value = value
        self._freeze()

    @classmethod
    def from_version(cls, version: ReleaseVersion) -> "ReleaseBranchName":
        return cls(f"{cls.PREFIX}{version.value}")

    @property
    def value(self) -> str:
        return self._value

    def _equality_components(self) -> tuple[Hashable, ...]:
        return (self._value,)
