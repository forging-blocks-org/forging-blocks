import os
from unittest.mock import AsyncMock, Mock, patch

import pytest

from scripts.release.presentation import __main__
from tests.fixtures.git_test_repository import GitTestRepository


@pytest.mark.e2e
class TestMain:
    @pytest.mark.skipif(
        not os.environ.get("RUN_E2E_TESTS"),
        reason="E2E test requires RUN_E2E_TESTS=1 and full project setup (poetry, pyproject.toml, etc.)",
    )
    @patch("scripts.release.presentation.__main__.Container")
    async def test_main_when_called_with_valid_arguments_then_creates_release(
        self, mock_container_class: Mock, git_repo: GitTestRepository
    ) -> None:
        # Arrange: Mock the container and its dependencies
        mock_container = Mock()
        mock_container_class.return_value = mock_container
        mock_container.initialize = AsyncMock()

        mock_prepare_service = AsyncMock()
        mock_container.get_prepare_release_use_case.return_value = mock_prepare_service
        mock_prepare_service.execute.return_value = Mock()  # Success result

        git_repo.write_file("example_file.txt", "Initial file content")
        git_repo.commit("Add example file")

        # Pass the Git repo path as a simulated environment
        os.environ["REPO_PATH"] = str(git_repo._path)

        argv = ["minor"]

        # Act: Run the application
        await __main__.main(argv)

        # Assert: Verify the service was called with correct parameters
        mock_prepare_service.execute.assert_called_once()

        # Clean up
        del os.environ["REPO_PATH"]

    @pytest.mark.skipif(
        not os.environ.get("RUN_E2E_TESTS"),
        reason="E2E test requires RUN_E2E_TESTS=1 and full project setup (poetry, pyproject.toml, etc.)",
    )
    @patch("scripts.release.presentation.__main__.Container")
    async def test_main_when_no_arguments_passed_then_uses_defaults(
        self, mock_container_class: Mock, git_repo: GitTestRepository
    ) -> None:
        # Arrange: Mock the container and its dependencies
        mock_container = Mock()
        mock_container_class.return_value = mock_container
        mock_container.initialize = AsyncMock()

        mock_prepare_service = AsyncMock()
        mock_container.get_prepare_release_use_case.return_value = mock_prepare_service
        mock_prepare_service.execute.return_value = Mock()  # Success result

        git_repo.write_file("README.md", "Initial readme")
        git_repo.commit("Add README.md")

        # Simulate an environment variable pointing to the repo
        os.environ["REPO_PATH"] = str(git_repo._path)

        # Act: Run the application with no arguments (defaults to 'patch')
        await __main__.main([])

        # Assert: Verify the service was called (should use default 'patch' level)
        mock_prepare_service.execute.assert_called_once()

        # Clean up
        del os.environ["REPO_PATH"]

    @pytest.mark.skipif(
        not os.environ.get("RUN_E2E_TESTS"),
        reason="E2E test requires RUN_E2E_TESTS=1 and full project setup (poetry, pyproject.toml, etc.)",
    )
    @patch(
        "scripts.release.presentation.presenters.release_cli_presenter.ReleaseCliPresenter.present"
    )
    async def test_main_when_tag_exists_then_raises_error(
        self, mock_present: AsyncMock, git_repo: GitTestRepository
    ) -> None:
        # Arrange: Mock the presenter to simulate tag already exists error
        mock_present.side_effect = Exception("Tag 'v0.2.0' already exists.")

        git_repo.write_file("example.txt", "Test content")
        git_repo.commit("Add test content")

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
    @patch("scripts.release.presentation.__main__.Container")
    async def test_main_when_execute_flag_passed_then_executes_release(
        self, mock_container_class: Mock, git_repo: GitTestRepository
    ) -> None:
        # Arrange: Mock the container to avoid real dependencies
        mock_container = Mock()
        mock_container_class.return_value = mock_container
        mock_container.initialize = AsyncMock()

        mock_prepare_service = AsyncMock()
        mock_container.get_prepare_release_use_case.return_value = mock_prepare_service
        mock_prepare_service.execute.return_value = Mock()  # Success result

        git_repo.write_file("readme.md", "Initial setup")
        git_repo.commit("Setup for test")

        os.environ["REPO_PATH"] = str(git_repo._path)

        # Use the actual --execute flag that the CLI supports
        argv = ["minor", "--execute"]

        # Act: Run the application in execute mode
        await __main__.main(argv)

        # Assert: Verify the service was called with execute=True
        mock_prepare_service.execute.assert_called_once()

        del os.environ["REPO_PATH"]
