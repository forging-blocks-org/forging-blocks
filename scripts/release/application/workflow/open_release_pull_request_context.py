from dataclasses import dataclass

from release.domain.entities.release_pull_request import ReleasePullRequest


@dataclass(frozen=True)
class OpenReleasePullRequestContext:
    pull_request: ReleasePullRequest
    dry_run: bool
