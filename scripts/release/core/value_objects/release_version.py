from __future__ import annotations

from typing import Hashable
from forging_blocks.domain import ValueObject

from ..errors.invalid_release_version_error import InvalidReleaseVersionError


class ReleaseVersion(ValueObject[str]):
    __slots__ = ("_major", "_minor", "_patch")

    def __init__(self, major: int, minor: int, patch: int) -> None:
        super().__init__()

        if min(major, minor, patch) < 0:
            raise InvalidReleaseVersionError(f"{major}.{minor}.{patch}")

        self._major = major
        self._minor = minor
        self._patch = patch
        self._freeze()

    @property
    def value(self) -> str:
        return f"{self._major}.{self._minor}.{self._patch}"

    @property
    def major(self) -> int:
        return self._major

    @property
    def minor(self) -> int:
        return self._minor

    @property
    def patch(self) -> int:
        return self._patch

    def _equality_components(self) -> tuple[Hashable, ...]:
        return (self._major, self._minor, self._patch)
