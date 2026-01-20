from __future__ import annotations

from scripts.release.application.services.open_release_pull_request_service import (
    OpenReleasePullRequestService,
)
from scripts.release.application.services.prepare_release_service import (
    PrepareReleaseService,
)
from scripts.release.infrastructure.bus.in_memory_release_event_bus import (
    InMemoryReleaseEventBus,
)
from scripts.release.infrastructure.git.git_changelog_generator import (
    GitChangelogGenerator,
)
from scripts.release.infrastructure.github.github_cli_pull_request_service import (
    GitHubCliPullRequestService,
)
from scripts.release.infrastructure.transactions.in_memory_release_transaction import (
    InMemoryReleaseTransaction,
)
from scripts.release.infrastructure.git.git_version_control import GitVersionControl
from scripts.release.infrastructure.versioning.poetry_versioning_service import (
    PoetryVersioningService,
)
from scripts.release.infrastructure.commons.process import (
    SubprocessCommandRunner,
)


class Container:
    """
    Minimal composition root for the release automation CLI.

    Notes:
    - Keep this module free of any CLI parsing concerns.
    - Keep it free of domain rules (those belong in domain / application).
    """

    @property
    def _command_runner(self) -> SubprocessCommandRunner:
        return SubprocessCommandRunner()

    def get_prepare_release_use_case(self) -> PrepareReleaseService:
        command_runner = self._command_runner

        return PrepareReleaseService(
            versioning_service=PoetryVersioningService(command_runner),
            version_control=GitVersionControl(command_runner),
            changelog_generator=GitChangelogGenerator(command_runner),
            transaction=InMemoryReleaseTransaction(),
            message_bus=InMemoryReleaseEventBus(),
        )

    def get_open_release_pull_request_use_case(self) -> OpenReleasePullRequestService:
        command_runner = self._command_runner

        return OpenReleasePullRequestService(
            pull_request_service=GitHubCliPullRequestService(command_runner ),
        )
