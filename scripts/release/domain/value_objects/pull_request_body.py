from typing import Hashable

from forging_blocks.domain import ValueObject


class PullRequestBody(ValueObject[str]):
    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        super().__init__()
        self._value = value
        self._freeze()

    @property
    def value(self) -> str:
        return self._value

    def _equality_components(self) -> tuple[Hashable, ...]:
        return (self._value,)
