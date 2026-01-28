from scripts.release.application.ports.inbound import (
    OpenReleasePullRequestInput,
    OpenReleasePullRequestOutput,
    OpenReleasePullRequestUseCase,
)
from scripts.release.application.ports.outbound import (
    PullRequestService,
)
from scripts.release.domain.entities import ReleasePullRequest
from scripts.release.domain.value_objects import (
    ReleaseBranchName,
    ReleaseVersion,
)


class OpenReleasePullRequestService(OpenReleasePullRequestUseCase):
    """Application service responsible for opening the release pull request.

    Responsibilities:
    - validate raw inputs
    - build ReleasePullRequest entity
    - delegate to infrastructure
    """

    def __init__(
        self,
        *,
        pull_request_service: PullRequestService,
    ) -> None:
        self._pull_request_service = pull_request_service

    async def execute(
        self,
        request: OpenReleasePullRequestInput,
    ) -> OpenReleasePullRequestOutput:
        pull_request = self._build_release_pull_request(request)

        if request.dry_run:
            return OpenReleasePullRequestOutput(
                pr_id=None,
                url=None,
            )

        output = self._pull_request_service.open(pull_request)

        return OpenReleasePullRequestOutput(
            pr_id=output.pr_id,
            url=output.url,
        )

    def _build_release_pull_request(
        self,
        request: OpenReleasePullRequestInput,
    ) -> ReleasePullRequest:
        release_version = ReleaseVersion.from_str(request.version)
        branch = ReleaseBranchName(request.branch)

        return ReleasePullRequest(
            base="main",
            head=branch,
            title=f"Release v{release_version.value}",
            body=f"Automated release pull request for version {release_version.value}.",
        )
