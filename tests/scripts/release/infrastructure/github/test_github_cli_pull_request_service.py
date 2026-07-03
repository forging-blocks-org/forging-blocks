# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
from __future__ import annotations

import os
import random

import pytest
from scripts.release.infrastructure.github.github_cli_pull_request_service import (
    GitHubCliPullRequestService,
)

from scripts.release.domain.entities import ReleasePullRequest
from scripts.release.domain.value_objects import ReleaseBranchName
from tests.fixtures.fake_command_runner import FakeCommandRunner


@pytest.mark.integration
class TestGitHubCliPullRequestServiceIntegration:
    @pytest.mark.skipif(
        not os.environ.get("RUN_GITHUB_CLI_TESTS"),
        reason="Requires RUN_GITHUB_CLI_TESTS=1 and authenticated GitHub CLI",
    )
    def test_open_when_called_then_pull_request_created(self) -> None:
        runner = FakeCommandRunner("https://github.com/forging-blocks-org/forging-blocks/pull/123")

        patch_version = random.randint(1000, 9999)
        branch = ReleaseBranchName(f"release/v0.0.{patch_version}")

        service = GitHubCliPullRequestService(runner=runner)
        pull_request = ReleasePullRequest(
            base="main",
            head=branch,
            title="CLI Integration Test",
            body="Automated infrastructure test",
        )

        output = service.open(pull_request)

        assert output.url == "https://github.com/forging-blocks-org/forging-blocks/pull/123"
        assert output.pr_id == "123"

        expected_cmd = [
            "gh",
            "pr",
            "create",
            "--base",
            "main",
            "--head",
            f"release/v0.0.{patch_version}",
            "--title",
            "CLI Integration Test",
            "--body",
            "Automated infrastructure test",
        ]
        assert len(runner.calls) == 1
        assert runner.calls[0][0] == expected_cmd
