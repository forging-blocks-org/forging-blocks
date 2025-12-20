from scripts.release.infrastructure.commons.process import run
from scripts.release.application.ports.outbound import (
    PullRequestService,
    CreatePullRequestInput,
    CreatePullRequestOutput,
)


class GitHubCliPullRequestService(PullRequestService):
    def create(self, input: CreatePullRequestInput) -> CreatePullRequestOutput:
        if input.dry_run:
            return CreatePullRequestOutput(
                pr_id=None,
                url=None,
            )

        url = run(
            [
                "gh",
                "pr",
                "create",
                "--base",
                input.base.value,
                "--head",
                input.head.value,
                "--title",
                input.title.value,
                "--body",
                input.body.value,
            ]
        )

        pr_id = url.rstrip("/").split("/")[-1]

        return CreatePullRequestOutput(
            pr_id=pr_id,
            url=url,
        )
