from typing import Hashable

from forging_blocks.domain import ValueObject


class PullRequestBase(ValueObject[str]):
    __slots__ = ("_value",)

    MAIN = "main"

    def __init__(self, value: str) -> None:
        super().__init__()
        self._value = value
        self._freeze()

    def is_main(self) -> bool:
        return self._value == self.MAIN

    @property
    def value(self) -> str:
        return self._value

    def _equality_components(self) -> tuple[Hashable, ...]:
        return (self._value,)
