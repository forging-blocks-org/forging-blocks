from __future__ import annotations

from typing import Hashable
from forging_blocks.domain import ValueObject

from .release_version import ReleaseVersion
from ..errors import InvalidReleaseBranchNameError


class ReleaseBranchName(ValueObject[str]):
    __slots__ = ("_value",)

    PREFIX = "release/v"

    def __init__(self, value: str) -> None:
        super().__init__()

        if not value.startswith(self.PREFIX):
            raise InvalidReleaseBranchNameError()

        self._value = value
        self._freeze()

    @classmethod
    def from_version(cls, version: ReleaseVersion) -> ReleaseBranchName:
        return cls(f"{cls.PREFIX}{version.value}")

    @property
    def value(self) -> str:
        return self._value

    def _equality_components(self) -> tuple[Hashable, ...]:
        return (self._value,)
