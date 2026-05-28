"""Outbound port for generating changelogs between versions."""

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any

from forging_blocks.foundation.ports import OutboundPort


@dataclass(frozen=True)
class ChangelogRequest:
    """Request DTO for changelog generation."""

    from_version: str
    dry_run: bool = field(default=False)


@dataclass(frozen=True)
class ChangelogResponse:
    """Response DTO for changelog generation."""

    entries: list[str]
    raw: str = field(default="")


class ChangelogGenerator(OutboundPort[Any, Any]):
    """Port for generating changelogs between versions."""

    @abstractmethod
    async def generate(self, request: ChangelogRequest) -> ChangelogResponse:
        """Generate a changelog between two versions.

        When ``dry_run`` is True the changelog is generated but not written
        to disk, allowing validation before a release.
        """
        ...
