from scripts.release.infrastructure.commons.process import CommandRunner, SubprocessCommandRunner
from scripts.release.application.ports.outbound import (
    PullRequestService,
    OpenPullRequestInput,
    OpenPullRequestOutput,
)


class GitHubCliPullRequestService(PullRequestService):
    def __init__(self, runner: CommandRunner | None = None) -> None:
        self._runner = runner if runner is not None else SubprocessCommandRunner()

    def open(self, input: OpenPullRequestInput) -> OpenPullRequestOutput:
        url = self._runner.run(
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

        return OpenPullRequestOutput(
            pr_id=pr_id,
            url=url,
        )
