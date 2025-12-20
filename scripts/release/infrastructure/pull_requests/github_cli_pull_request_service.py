from scripts.release.infrastructure.commons.process import run
from scripts.release.application.ports.outbound import (
    PullRequestService,
    PullRequestServiceOutput,
)
from scripts.release.domain.value_objects import (
    PullRequestBase,
    PullRequestHead,
    PullRequestTitle,
    PullRequestBody,
)


class GitHubCliPullRequestService(PullRequestService):
    def create(
        self,
        *,
        base: PullRequestBase,
        head: PullRequestHead,
        title: PullRequestTitle,
        body: PullRequestBody,
        dry_run: bool,
    ) -> PullRequestServiceOutput:
        if dry_run:
            return PullRequestServiceOutput(
                pr_id=None,
                url=None,
            )

        url = run(
            [
                "gh",
                "pr",
                "create",
                "--base",
                base.value,
                "--head",
                head.value,
                "--title",
                title.value,
                "--body",
                body.value,
            ]
        )

        pr_id = url.rstrip("/").split("/")[-1]

        return PullRequestServiceOutput(
            pr_id=pr_id,
            url=url,
        )
