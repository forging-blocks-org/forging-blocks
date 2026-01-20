from __future__ import annotations

from typing import Hashable

from forging_blocks.domain import ValueObject

from scripts.release.domain.value_objects.common import ReleaseLevelEnum
from scripts.release.domain.errors import InvalidReleaseLevelError


class ReleaseLevel(ValueObject[str]):
    __slots__ = ("_level",)

    def __init__(self, level: ReleaseLevelEnum) -> None:
        super().__init__()
        self._level = level
        self._freeze()

    @classmethod
    def from_str(cls, value: str) -> ReleaseLevel:
        if value.lower() not in ReleaseLevelEnum:
            raise InvalidReleaseLevelError(value)
        return cls(ReleaseLevelEnum[value.upper()])

    @property
    def value(self) -> str:
        return self._level.value

    def _equality_components(self) -> tuple[Hashable, ...]:
        return (self._level,)
