from typing import Hashable

from forging_blocks.domain import ValueObject
from scripts.release.domain.errors import InvalidReleaseVersionError, InvalidTagNameError
from scripts.release.domain.value_objects import ReleaseVersion


class TagName(ValueObject[str]):
    __slots__ = ("_value",)

    PREFIX = "v"

    def __init__(self, value: str) -> None:
        super().__init__()

        if not value.startswith(self.PREFIX):
            raise InvalidTagNameError(value)

        version_part = value[len(self.PREFIX) :]
        parts = version_part.split(".")

        if len(parts) != 3:
            raise InvalidTagNameError(value)

        try:
            major, minor, patch = (int(p) for p in parts)
        except ValueError as exc:
            raise InvalidTagNameError(value) from exc

        try:
            ReleaseVersion(major, minor, patch)
        except InvalidReleaseVersionError as exc:
            raise InvalidTagNameError(value) from exc

        self._value = value
        self._freeze()

    @classmethod
    def for_version(cls, version: ReleaseVersion) -> "TagName":
        return cls(f"{cls.PREFIX}{version.value}")

    @property
    def value(self) -> str:
        return self._value

    def _equality_components(self) -> tuple[Hashable, ...]:
        return (self._value,)
