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
    Application service responsible for creating a release pull request.

    Responsibilities:
    - validate raw inputs
    - convert primitives into Value Objects
    - enforce domain invariants
    - delegate PR creation to infrastructure
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
        # 1. Convert primitives → Value Objects
        base = PullRequestBase(request.base)
        release_branch_name = ReleaseBranchName(request.head)
        head = PullRequestHead(release_branch_name)
        title = PullRequestTitle(request.title)
        body = PullRequestBody(request.body)

        # 2. Enforce domain invariants (entity as validation boundary)
        _ = ReleasePullRequest(
            base=base,
            head=head,
            title=title,
            body=body,
        )

        # 3. Dry-run: no side effects
        if request.dry_run:
            return OpenReleasePullRequestOutput(
                pr_id=None,
                url=None,
            )

        # 4. Delegate to infrastructure
        open_pull_request_input = OpenPullRequestInput(
            base=base,
            head=head,
            title=title,
            body=body,
            dry_run=False,
        )
        pull_request_service_output = self._pull_request_service.open(
            open_pull_request_input
        )

        return OpenReleasePullRequestOutput(
            pr_id=pull_request_service_output.pr_id,
            url=pull_request_service_output.url,
        )
