from typing import TypeAlias

from forging_blocks.domain.messages.command import Command

PayloadType: TypeAlias = dict[str, str | bool]


class OpenPullRequestCommand(Command[PayloadType]):
    def __init__(self, *, version: str, branch: str, dry_run: bool) -> None:
        self._version = version
        self._branch = branch
        self._dry_run = dry_run
        self._value = {"version": self._version, "branch": self._branch, "dry_run": self._dry_run}

        super().__init__()

    @property
    def value(self) -> PayloadType:
        return self._value

    @property
    def version(self) -> str:
        return self._version

    @property
    def branch(self) -> str:
        return self._branch

    @property
    def dry_run(self) -> bool:
        return self._dry_run

    @property
    def _payload(self) -> PayloadType:
        return self._value
