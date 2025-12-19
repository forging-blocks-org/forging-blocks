from scripts.release.application.ports.inbound import (
    CreateReleasePullRequestUseCase,
    CreateReleasePullRequestInput,
    CreateReleasePullRequestOutput,
)
from scripts.release.application.ports.outbound import PullRequestService
from scripts.release.domain.entities import ReleasePullRequest
from scripts.release.domain.value_objects import (
    PullRequestBase,
    PullRequestHead,
    PullRequestTitle,
    PullRequestBody,
    ReleaseBranchName,
)


class CreateReleasePullRequestService(CreateReleasePullRequestUseCase):
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
        request: CreateReleasePullRequestInput,
    ) -> CreateReleasePullRequestOutput:
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
            return CreateReleasePullRequestOutput(
                pr_id=None,
                url=None,
            )

        # 4. Delegate to infrastructure
        pull_request_service_output = self._pull_request_service.create(
            base=base,
            head=head,
            title=title,
            body=body,
            dry_run=False,
        )

        return CreateReleasePullRequestOutput(
            pr_id=pull_request_service_output.pr_id,
            url=pull_request_service_output.url,
        )
