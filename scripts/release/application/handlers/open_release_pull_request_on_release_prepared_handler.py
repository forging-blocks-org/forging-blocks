from scripts.release.application.ports.inbound import OpenReleasePullRequestInput, OpenReleasePullRequestUseCase, ReleasePreparedHandler
from scripts.release.domain.events.release_prepared_event import ReleasePreparedEvent


class OpenReleasePullRequestOnReleasePreparedHandler(ReleasePreparedHandler):
    """
    Event handler that opens a release pull request when a release is prepared.
    Responsibilities:
    - Listen for ReleasePreparedEvent events.
    - Construct the PR input from the event data.
    - Delegate the PR creation to the OpenReleasePullRequestUseCase.
    - Ensure no side effects beyond the use case.
    """
    def __init__(self, use_case: OpenReleasePullRequestUseCase):
        self._use_case = use_case

    async def handle(self, event: ReleasePreparedEvent) -> None:
        version = event.value.get("version")
        branch = event.value.get("branch")
        dry_run = event.value.get("dry_run")

        assert version
        assert branch
        assert dry_run

        pr_input = OpenReleasePullRequestInput(
            version=version,
            branch=branch,
            dry_run=dry_run,
        )

        await self._use_case.execute(pr_input)
