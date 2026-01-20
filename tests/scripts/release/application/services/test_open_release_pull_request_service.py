import pytest
from unittest.mock import Mock

from scripts.release.application.ports.outbound import OpenPullRequestOutput, PullRequestService
from scripts.release.application.services.open_release_pull_request_service import (
    OpenReleasePullRequestService,
)
from scripts.release.application.ports.inbound import (
    OpenReleasePullRequestInput,
)
from scripts.release.domain.errors import InvalidReleasePullRequestError


class TestOpenReleasePullRequestService:
    async def test_execute_when_dry_run_then_no_infra_call(self) -> None:
        pull_request_service = Mock(spec=PullRequestService)

        service = OpenReleasePullRequestService(
            pull_request_service=pull_request_service,
        )

        result = await service.execute(
            OpenReleasePullRequestInput(
                version="1.2.3",
                branch="release/v1.2.3",
                dry_run=True,
            )
        )

        assert result.pr_id is None
        assert result.url is None
        pull_request_service.open.assert_not_called()

    async def test_execute_when_valid_then_delegate_to_infrastructure(self) -> None:
        pull_request_service = Mock(spec=PullRequestService)
        pull_request_service.open.return_value = OpenPullRequestOutput(
            pr_id="123",
            url="https://example/pr/123",
        )

        service = OpenReleasePullRequestService(
            pull_request_service=pull_request_service,
        )

        result = await service.execute(
            OpenReleasePullRequestInput(
                version="1.2.3",
                branch="release/v1.2.3",
                dry_run=False,
            )
        )

        assert result.pr_id == "123"
        assert result.url
        assert result.url.endswith("/123")
        pull_request_service.open.assert_called_once()

    async def test_execute_when_domain_invariant_violated_then_error(self) -> None:
        service = OpenReleasePullRequestService(
            pull_request_service=Mock(spec=PullRequestService),
        )

        with pytest.raises(InvalidReleasePullRequestError):
            await service.execute(
                OpenReleasePullRequestInput(
                    version="invalid-version",
                    branch="release/invalid-branch",
                    dry_run=False,
                )
            )
