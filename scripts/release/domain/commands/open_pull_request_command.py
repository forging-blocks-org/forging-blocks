from typing import Self, TypeAlias, cast

from forging_blocks.domain.messages.command import Command
from forging_blocks.domain.messages.message import MessageMetadata

PayloadType: TypeAlias = dict[str, str | bool]


class OpenPullRequestCommand(Command[PayloadType]):
    def __init__(
        self, *, version: str, branch: str, dry_run: bool, metadata: MessageMetadata | None = None
    ) -> None:
        self._version = version
        self._branch = branch
        self._dry_run = dry_run
        self._value: PayloadType = {
            "version": self._version,
            "branch": self._branch,
            "dry_run": self._dry_run,
        }

        super().__init__(metadata)

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
    def _payload(self) -> dict[str, object]:
        return cast(dict[str, object], self._value)

    @classmethod
    def from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        """Reconstruct from payload fields and metadata."""
        return cls(
            version=str(data["version"]),
            branch=str(data["branch"]),
            dry_run=bool(data["dry_run"]),
            metadata=metadata,
        )
