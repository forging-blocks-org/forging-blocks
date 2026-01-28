"""Outbound port for generating changelogs between versions."""

from abc import abstractmethod
from dataclasses import dataclass

from forging_blocks.foundation.ports import OutboundPort


@dataclass(frozen=True)
class ChangelogRequest:
    """Request DTO for changelog generation."""

    from_version: str  # The starting version


@dataclass(frozen=True)
class ChangelogResponse:
    """Response DTO for changelog generation."""

    entries: list[str]  # List of changelog entries


class ChangelogGenerator(OutboundPort):
    """Port for generating changelogs between versions."""

    @abstractmethod
    async def generate(self, request: ChangelogRequest) -> ChangelogResponse:
        """
        Generate a changelog between two versions.

        Args:
            request (ChangelogRequest): The request containing from and to versions.
        Returns:
            ChangelogResponse: The generated changelog entries.
        """
        ...
