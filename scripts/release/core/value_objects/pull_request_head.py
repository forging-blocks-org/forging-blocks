from typing import Hashable

from forging_blocks.domain import ValueObject

from scripts.release.core.value_objects import ReleaseBranchName


class PullRequestHead(ValueObject[str]):
    __slots__ = ("_branch",)

    def __init__(self, branch: ReleaseBranchName) -> None:
        super().__init__()
        self._branch = branch
        self._freeze()

    def is_release_branch(self) -> bool:
        return True  # semantic guarantee by construction

    @property
    def value(self) -> str:
        return self._branch.value

    def _equality_components(self) -> tuple[Hashable, ...]:
        return (self._branch,)
