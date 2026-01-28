"""Tests for the improved error handling in release CLI presenter."""

from unittest.mock import AsyncMock, Mock, patch

from scripts.release.application.errors.release_branch_exists_error import ReleaseBranchExistsError
from scripts.release.application.errors.tag_already_exists_error import TagAlreadyExistsError
from scripts.release.presentation.presenters.release_cli_presenter import ReleaseCliPresenter


class TestReleaseCliPresenterErrorHandling:
    """Test the improved error handling in the release CLI presenter."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_parser = Mock()
        self.mock_container = Mock()
        self.presenter = ReleaseCliPresenter(self.mock_parser, self.mock_container)

    @patch("sys.exit")
    @patch("builtins.print")
    def test_handle_branch_exists_error(self, mock_print, mock_exit):
        """Test handling of branch already exists error."""
        error = ReleaseBranchExistsError("release/v0.3.11")

        self.presenter._handle_branch_exists_error(error)

        # Verify user-friendly error message is printed
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert "\n❌ Release Failed: Branch already exists with these changes" in print_calls
        assert "   Branch 'release/v0.3.11' already contains the release artifacts." in print_calls
        assert "git branch -D release/v0.3.11" in str(print_calls)
        assert "git push origin --delete release/v0.3.11" in str(print_calls)

        # Verify exit is called with error code 1
        mock_exit.assert_called_once_with(1)

    @patch("sys.exit")
    @patch("builtins.print")
    def test_handle_tag_exists_error(self, mock_print, mock_exit):
        """Test handling of tag already exists error."""
        error = TagAlreadyExistsError("v0.3.11")

        self.presenter._handle_tag_exists_error(error)

        # Verify user-friendly error message is printed
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert "\n❌ Release Failed: Tag already exists" in print_calls
        # The error is printed as its string representation
        assert "'v0.3.11' already exists" in str(print_calls)

        # Verify exit is called with error code 1
        mock_exit.assert_called_once_with(1)

    @patch("sys.exit")
    @patch("builtins.print")
    def test_handle_git_commit_nothing_to_commit_error(self, mock_print, mock_exit):
        """Test handling of git commit with nothing to commit error."""
        error = RuntimeError(
            "Command failed: git commit -am message\nnothing to commit, working tree clean"
        )

        self.presenter._handle_command_error(error)

        # Verify user-friendly error message is printed
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert "\n❌ Release Failed: Nothing to commit" in print_calls
        assert "   The release branch already exists with the same changes." in print_calls

        # Verify exit is called with error code 1
        mock_exit.assert_called_once_with(1)

    @patch("sys.exit")
    @patch("builtins.print")
    def test_handle_git_push_error(self, mock_print, mock_exit):
        """Test handling of git push error."""
        error = RuntimeError("Command failed: git push origin branch\nremote: Permission denied")

        self.presenter._handle_command_error(error)

        # Verify user-friendly error message is printed
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert "\n❌ Release Failed: Git push error" in print_calls
        assert "   Could not push release branch to remote." in print_calls
        assert "Check network connection" in str(print_calls)

        # Verify exit is called with error code 1
        mock_exit.assert_called_once_with(1)

    @patch("sys.exit")
    @patch("builtins.print")
    def test_handle_github_pr_error(self, mock_print, mock_exit):
        """Test handling of GitHub PR creation error."""
        error = RuntimeError("Command failed: gh pr create\ngh: command not found")

        self.presenter._handle_command_error(error)

        # Verify user-friendly error message is printed
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert "\n❌ Release Failed: Pull request creation error" in print_calls
        assert "   Could not create pull request." in print_calls
        assert "Install GitHub CLI: gh --version" in str(print_calls)

        # Verify exit is called with error code 1
        mock_exit.assert_called_once_with(1)

    @patch("sys.exit")
    @patch("builtins.print")
    def test_handle_unexpected_error(self, mock_print, mock_exit):
        """Test handling of unexpected errors."""
        error = ValueError("Some unexpected error")

        self.presenter._handle_unexpected_error(error)

        # Verify user-friendly error message is printed
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert "\n❌ Release Failed: Unexpected error" in print_calls
        assert "   ValueError: Some unexpected error" in print_calls
        assert "Check if all dependencies are installed" in str(print_calls)

        # Verify exit is called with error code 1
        mock_exit.assert_called_once_with(1)

    def test_extract_user_friendly_message(self):
        """Test extraction of user-friendly messages from error output."""
        error_msg = "Command failed: git commit\nSome error details\n  Traceback info"

        result = self.presenter._extract_user_friendly_message(error_msg)

        assert result == "Command failed: git commit"

    def test_extract_user_friendly_message_long_message(self):
        """Test extraction handles long messages by truncating."""
        long_msg = "x" * 300

        result = self.presenter._extract_user_friendly_message(long_msg)

        assert len(result) <= 203  # 200 + "..."
        assert result.endswith("...")


class TestReleaseCliPresenterIntegration:
    """Test the release CLI presenter with actual error scenarios."""

    @patch("sys.exit")
    @patch("builtins.print")
    async def test_present_with_tag_already_exists_error(self, mock_print, mock_exit):
        """Test the present method when TagAlreadyExistsError occurs."""
        mock_parser = Mock()
        mock_container = Mock()

        # Setup parser to return valid input
        mock_parsed_input = Mock()
        mock_parsed_input.level = "patch"
        mock_parsed_input.execute = True
        mock_parser.parse.return_value = mock_parsed_input

        # Setup use case to raise TagAlreadyExistsError
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = TagAlreadyExistsError("v0.3.11")
        mock_container.get_prepare_release_use_case.return_value = mock_use_case

        presenter = ReleaseCliPresenter(mock_parser, mock_container)

        # Call present method - it should handle the error gracefully
        await presenter.present()

        # Verify error handling was triggered
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert "\n❌ Release Failed: Tag already exists" in print_calls
        mock_exit.assert_called_once_with(1)

    @patch("sys.exit")
    @patch("builtins.print")
    async def test_present_with_branch_exists_error(self, mock_print, mock_exit):
        """Test the present method when ReleaseBranchExistsError occurs."""
        mock_parser = Mock()
        mock_container = Mock()

        # Setup parser to return valid input
        mock_parsed_input = Mock()
        mock_parsed_input.level = "patch"
        mock_parsed_input.execute = True
        mock_parser.parse.return_value = mock_parsed_input

        # Setup use case to raise ReleaseBranchExistsError
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = ReleaseBranchExistsError("release/v0.3.11")
        mock_container.get_prepare_release_use_case.return_value = mock_use_case

        presenter = ReleaseCliPresenter(mock_parser, mock_container)

        # Call present method - it should handle the error gracefully
        await presenter.present()

        # Verify error handling was triggered
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert "\n❌ Release Failed: Branch already exists with these changes" in print_calls
        mock_exit.assert_called_once_with(1)

    @patch("sys.exit")
    @patch("builtins.print")
    async def test_present_with_runtime_error(self, mock_print, mock_exit):
        """Test the present method when RuntimeError occurs."""
        mock_parser = Mock()
        mock_container = Mock()

        # Setup parser to return valid input
        mock_parsed_input = Mock()
        mock_parsed_input.level = "patch"
        mock_parsed_input.execute = True
        mock_parser.parse.return_value = mock_parsed_input

        # Setup use case to raise RuntimeError
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = RuntimeError(
            "Command failed: git commit -am message\nnothing to commit"
        )
        mock_container.get_prepare_release_use_case.return_value = mock_use_case

        presenter = ReleaseCliPresenter(mock_parser, mock_container)

        # Call present method - it should handle the error gracefully
        await presenter.present()

        # Verify error handling was triggered
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert "\n❌ Release Failed: Nothing to commit" in print_calls
        mock_exit.assert_called_once_with(1)

    @patch("sys.exit")
    @patch("builtins.print")
    async def test_present_with_unexpected_error(self, mock_print, mock_exit):
        """Test the present method when unexpected Exception occurs."""
        mock_parser = Mock()
        mock_container = Mock()

        # Setup parser to return valid input
        mock_parsed_input = Mock()
        mock_parsed_input.level = "patch"
        mock_parsed_input.execute = True
        mock_parser.parse.return_value = mock_parsed_input

        # Setup use case to raise unexpected error
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = ValueError("Some unexpected error")
        mock_container.get_prepare_release_use_case.return_value = mock_use_case

        presenter = ReleaseCliPresenter(mock_parser, mock_container)

        # Call present method - it should handle the error gracefully
        await presenter.present()

        # Verify error handling was triggered
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert "\n❌ Release Failed: Unexpected error" in print_calls
        mock_exit.assert_called_once_with(1)
