from typing import Hashable

from forging_blocks.domain import ValueObject

from scripts.release.domain.errors.invalid_pull_request_title_error import (
    InvalidPullRequestTitleError,
)
from scripts.release.domain.value_objects.common import PullRequestTitleLengthBoundaries


class PullRequestTitle(ValueObject[str]):
    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        super().__init__()

        if not value:
            raise InvalidPullRequestTitleError(
                PullRequestTitleLengthBoundaries.MIN,
                PullRequestTitleLengthBoundaries.MAX,
            )

        length = len(value)

        if (
            length < PullRequestTitleLengthBoundaries.MIN
            or length > PullRequestTitleLengthBoundaries.MAX
        ):
            raise InvalidPullRequestTitleError(
                PullRequestTitleLengthBoundaries.MIN,
                PullRequestTitleLengthBoundaries.MAX,
            )

        self._value = value
        self._freeze()

    @property
    def value(self) -> str:
        return self._value

    def _equality_components(self) -> tuple[Hashable, ...]:
        return (self._value,)
