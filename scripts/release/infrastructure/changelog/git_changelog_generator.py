from scripts.release.application.ports.outbound.changelog_generator import (
    ChangelogGenerator,
    ChangelogRequest,
    ChangelogResponse,
)
from scripts.release.infrastructure.commons.process import run


class GitChangelogGenerator(ChangelogGenerator):
    async def generate(self, request: ChangelogRequest) -> ChangelogResponse:
        range_expr = f"v{request.from_version}..HEAD"

        stdout = run(
            [
                "git",
                "log",
                range_expr,
                "--pretty=format:- %s (%h)",
            ]
        )

        entries = [line.strip() for line in stdout.splitlines() if line.strip()]

        return ChangelogResponse(entries=entries)
