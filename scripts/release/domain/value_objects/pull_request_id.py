from __future__ import annotations

from typing import Hashable

from forging_blocks.domain.value_object import ValueObject
from forging_blocks.foundation.result import Err, Ok, Result
from release.domain.errors import InvalidPullRequestIdError


class PullRequestId(ValueObject[int]):
    __slots__ = ("_value",)

    def __init__(self, value: int) -> None:
        self._value = value
        self._freeze()

    @classmethod
    def create(cls, value: int | str) -> Result[PullRequestId, InvalidPullRequestIdError]:
        str_value = str(value)

        if not str_value.isdigit() or int(str_value) <= 0:
            return Err(InvalidPullRequestIdError(value))

        return Ok(cls(int(str_value)))

    @property
    def value(self) -> int:
        return self._value

    def _equality_components(self) -> tuple[Hashable, ...]:
        return (self._value,)
