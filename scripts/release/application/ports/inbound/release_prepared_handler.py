from typing import Protocol
from forging_blocks.application.ports.inbound.message_handler import EventHandler

from scripts.release.domain.events.release_prepared_event import ReleasePreparedEvent


class ReleasePreparedHandler(EventHandler[ReleasePreparedEvent], Protocol):
    async def handle(self, event: ReleasePreparedEvent) -> None:
        """
        Handle the ReleasePreparedEvent by creating a pull request.

        Args:
            event (ReleasePreparedEvent): Event that signals the release is prepared
                and contains the branch and version details.

        Responsibilities:
        - Construct the PR input from the event data.
        - Delegate the PR creation to the OpenReleasePullRequestUseCase.
        - Ensure no side effects beyond the use case.
        """
        pass
