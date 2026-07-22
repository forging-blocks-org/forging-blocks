from typing import Protocol

from scripts.release.application.ports.inbound import (
    OpenReleasePullRequestInput,
    OpenReleasePullRequestOutput,
)
from scripts.release.application.ports.inbound.open_pull_request_command_handler import (
    OpenPullRequestCommandHandler,
)
from scripts.release.domain.commands import OpenPullRequestCommand


class _ReleasePullRequestExecutor(Protocol):
    """Structural contract for creating a release pull request.

    Narrower than ``OpenReleasePullRequestUseCase`` — this is NOT an
    InboundPort, so command handlers may depend on it without violating
    the InboundPort → OutboundPort-only dependency rule.
    """

    async def execute(
        self,
        request: OpenReleasePullRequestInput,
    ) -> OpenReleasePullRequestOutput: ...


class OpenPullRequestHandler(OpenPullRequestCommandHandler):
    """Command handler that opens a release pull request when a release is prepared.
    Responsibilities:
    - Listen for ReleasePreparedCommand events.
    - Construct the PR input from the event data.
    - Delegate the PR creation to the OpenReleasePullRequestUseCase.
    - Ensure no side effects beyond the use case.
    """

    def __init__(self, use_case: _ReleasePullRequestExecutor):
        self._use_case = use_case

    async def handle(self, message: OpenPullRequestCommand) -> None:
        version = message.version
        branch = message.branch
        dry_run = message.dry_run

        pr_input = OpenReleasePullRequestInput(
            version=version,
            branch=branch,
            dry_run=dry_run,
        )

        await self._use_case.execute(pr_input)
