import os
import pytest
from pathlib import Path
from pytest import mark as pytest_marker

from scripts.release.presentation import __main__
from tests.fixtures.git_test_repository import GitTestRepository


@pytest.mark.e2e
class TestMain:
    @pytest.mark.skipif(
        not os.environ.get("RUN_E2E_TESTS"),
        reason="E2E test requires RUN_E2E_TESTS=1 and full project setup (poetry, pyproject.toml, etc.)",
    )
    async def test_main_when_called_with_valid_arguments_then_creates_release(
        self, git_repo: GitTestRepository
    ) -> None:
        # Arrange: Set up a temporary Git repository
        git_repo.write_file("example_file.txt", "Initial file content")
        git_repo.commit("Add example file")

        # Pass the Git repo path as a simulated environment
        os.environ["REPO_PATH"] = str(git_repo._path)

        argv = ["minor"]

        # Act: Run the application
        await __main__.main(argv)

        # Assert: Check that a new tag was created
        assert "v0.2.0" in git_repo.tags, "Expected tag v0.2.0 to be created"
        assert git_repo.last_commit_message() == "Bump version to v0.2.0"

        # Clean up
        del os.environ["REPO_PATH"]

    @pytest.mark.skipif(
        not os.environ.get("RUN_E2E_TESTS"),
        reason="E2E test requires RUN_E2E_TESTS=1 and full project setup (poetry, pyproject.toml, etc.)",
    )
    async def test_main_when_no_arguments_passed_then_uses_defaults(
        self, git_repo: GitTestRepository
    ) -> None:
        # Arrange: Initialize a Git repository without passing arguments
        git_repo.write_file("README.md", "Initial readme")
        git_repo.commit("Add README.md")

        # Simulate an environment variable pointing to the repo
        os.environ["REPO_PATH"] = str(git_repo._path)

        # Act: Run the application with no arguments
        await __main__.main()

        # Assert: Verify defaults were used (e.g., patch version bump, dry_run)
        assert git_repo.last_commit_message() == "Bump version to v0.1.1"

        # Clean up
        del os.environ["REPO_PATH"]

    @pytest.mark.skipif(
        not os.environ.get("RUN_E2E_TESTS"),
        reason="E2E test requires RUN_E2E_TESTS=1 and full project setup (poetry, pyproject.toml, etc.)",
    )
    async def test_main_when_tag_exists_then_raises_error(
        self, git_repo: GitTestRepository
    ) -> None:
        # Arrange
        git_repo.write_file("example.txt", "Test content")
        git_repo.commit("Add test content")
        git_repo.create_tag("v0.2.0")  # Simulate the tag already exists

        os.environ["REPO_PATH"] = str(git_repo._path)

        argv = ["minor"]

        # Act & Assert: Expect a failure due to the existing tag
        with pytest.raises(Exception, match="Tag 'v0.2.0' already exists."):
            await __main__.main(argv)

        del os.environ["REPO_PATH"]

    @pytest.mark.skipif(
        not os.environ.get("RUN_E2E_TESTS"),
        reason="E2E test requires RUN_E2E_TESTS=1 and full project setup (poetry, pyproject.toml, etc.)",
    )
    async def test_main_when_dry_run_then_does_not_modify_repo(
        self, git_repo: GitTestRepository
    ):
        # Arrange: Create a valid Git repository
        git_repo.write_file("readme.md", "Initial dry run setup")
        git_repo.commit("Setup for dry run")

        os.environ["REPO_PATH"] = str(git_repo._path)

        argv = ["minor", "--dry-run"]

        # Act: Run the application in dry-run mode
        await __main__.main(argv)

        # Assert: Ensure the repository did not change
        assert git_repo.last_commit_message() == "Setup for dry run"
        assert "v0.2.0" not in git_repo.tags

        del os.environ["REPO_PATH"]
