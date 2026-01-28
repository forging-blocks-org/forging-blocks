"""Tests for the ReleaseBranchExistsError."""

import pytest
from scripts.release.application.errors.release_branch_exists_error import ReleaseBranchExistsError


class TestReleaseBranchExistsError:
    """Test the ReleaseBranchExistsError class."""

    def test_error_creation(self):
        """Test that ReleaseBranchExistsError can be created with a branch name."""
        branch_name = "release/v0.3.11"
        error = ReleaseBranchExistsError(branch_name)

        assert error.branch_name == branch_name
        assert str(error) == f"Release branch '{branch_name}' already exists with the same changes"

    def test_error_inheritance(self):
        """Test that ReleaseBranchExistsError inherits from Exception."""
        error = ReleaseBranchExistsError("test-branch")

        assert isinstance(error, Exception)

    def test_error_can_be_raised_and_caught(self):
        """Test that the error can be raised and caught properly."""
        branch_name = "release/v1.0.0"

        with pytest.raises(ReleaseBranchExistsError) as exc_info:
            raise ReleaseBranchExistsError(branch_name)

        assert exc_info.value.branch_name == branch_name
        assert branch_name in str(exc_info.value)
