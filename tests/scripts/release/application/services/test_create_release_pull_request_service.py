import pytest
from unittest.mock import Mock

from scripts.release.application.services.create_release_pull_request_service import (
    CreateReleasePullRequestService,
)
from scripts.release.application.ports.inbound import (
    CreateReleasePullRequestInput,
)
from scripts.release.application.ports.outbound import (
    PullRequestService,
    PullRequestServiceOutput,
)
from scripts.release.domain.errors import InvalidReleasePullRequestError


class TestCreateReleasePullRequestService:
    async def test_execute_when_dry_run_then_no_infra_call(self) -> None:
        pull_request_service = Mock(spec=PullRequestService)

        service = CreateReleasePullRequestService(
            pull_request_service=pull_request_service,
        )

        result = await service.execute(
            CreateReleasePullRequestInput(
                base="main",
                head="release/v1.2.3",
                title="Release v1.2.3",
                body="Notes",
                dry_run=True,
            )
        )

        assert result.pr_id is None
        assert result.url is None
        pull_request_service.create.assert_not_called()

    async def test_execute_when_valid_then_delegate_to_infrastructure(self) -> None:
        pull_request_service = Mock(spec=PullRequestService)
        pull_request_service.create.return_value = PullRequestServiceOutput(
            pr_id="123",
            url="https://example/pr/123",
        )

        service = CreateReleasePullRequestService(
            pull_request_service=pull_request_service,
        )

        result = await service.execute(
            CreateReleasePullRequestInput(
                base="main",
                head="release/v1.2.3",
                title="Release v1.2.3",
                body="Notes",
                dry_run=False,
            )
        )

        assert result.pr_id == "123"
        assert result.url
        assert result.url.endswith("/123")
        pull_request_service.create.assert_called_once()

    async def test_execute_when_domain_invariant_violated_then_error(self) -> None:
        service = CreateReleasePullRequestService(
            pull_request_service=Mock(spec=PullRequestService),
        )

        with pytest.raises(InvalidReleasePullRequestError):
            await service.execute(
                CreateReleasePullRequestInput(
                    base="develop",
                    head="release/v1.2.3",
                    title="Release v1.2.3",
                    body="Notes",
                    dry_run=False,
                )
            )
