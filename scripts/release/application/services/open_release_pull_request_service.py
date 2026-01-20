from release.application.ports.outbound.pull_request_service import OpenPullRequestOutput
from release.application.workflow.open_release_pull_request_context import OpenReleasePullRequestContext
from release.domain.value_objects.release_version import ReleaseVersion
from scripts.release.application.ports.inbound import (
    OpenReleasePullRequestUseCase,
    OpenReleasePullRequestInput,
    OpenReleasePullRequestOutput,
)
from scripts.release.application.ports.outbound import (
    OpenPullRequestInput,
    PullRequestService,
)
from scripts.release.domain.entities import ReleasePullRequest
from scripts.release.domain.value_objects import (
    PullRequestBase,
    PullRequestHead,
    PullRequestTitle,
    PullRequestBody,
    ReleaseBranchName,
)


class OpenReleasePullRequestService(OpenReleasePullRequestUseCase):
    """
    Application service responsible for opening the release pull request.

    Responsibilities:
    - validate raw inputs
    - convert primitives into Value Objects
    - enforce domain invariants
    - derive PR metadata automatically
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
        context = self._build_context(request)

        if context.dry_run:
            return OpenReleasePullRequestOutput(
                pr_id=None,
                url=None,
            )

        return self._open_pull_request(context)

    def _build_context(
        self,
        request: OpenReleasePullRequestInput,
    ) -> OpenReleasePullRequestContext:
        pull_request = self._build_release_pull_request(request)

        return OpenReleasePullRequestContext(
            pull_request=pull_request,
            dry_run=request.dry_run,
        )

    def _build_release_pull_request(
        self,
        request: OpenReleasePullRequestInput,
    ) -> ReleasePullRequest:
        release_version = ReleaseVersion.from_str(request.version)
        branch = ReleaseBranchName(request.branch)

        base = PullRequestBase("main")
        head = PullRequestHead(branch)

        title = PullRequestTitle(f"Release v{release_version.value}")
        body = PullRequestBody(
            f"Automated release pull request for version {release_version.value}."
        )

        return ReleasePullRequest(
            base=base,
            head=head,
            title=title,
            body=body,
        )

    def _open_pull_request(
        self,
        context: OpenReleasePullRequestContext,
    ) -> OpenReleasePullRequestOutput:
        output = self._pull_request_service.open(
            OpenPullRequestInput(
                base=context.pull_request.base,
                head=context.pull_request.head,
                title=context.pull_request.title,
                body=context.pull_request.body,
            )
        )

        return OpenReleasePullRequestOutput(
            pr_id=output.pr_id,
            url=output.url,
        )
