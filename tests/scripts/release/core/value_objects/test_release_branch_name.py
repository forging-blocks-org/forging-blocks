import pytest

from scripts.release.core.value_objects.release_branch_name import (
    ReleaseBranchName,
)
from scripts.release.core.value_objects.release_version import ReleaseVersion
from scripts.release.core.errors import InvalidReleaseBranchNameError


class TestReleaseBranchName:
    def test_init_when_valid_branch_name_then_success(self) -> None:
        branch = ReleaseBranchName("release/v1.2.3")

        assert branch.value == "release/v1.2.3"

    def test_init_when_invalid_branch_name_then_error(self) -> None:
        with pytest.raises(InvalidReleaseBranchNameError):
            ReleaseBranchName("feature/add-login")

    def test_from_version_when_valid_version_then_branch_created(self) -> None:
        version = ReleaseVersion(1, 2, 3)

        branch = ReleaseBranchName.from_version(version)

        assert branch.value == "release/v1.2.3"

    def test_equality_components_when_same_value_then_equal(self) -> None:
        branch_1 = ReleaseBranchName("release/v2.0.0")
        branch_2 = ReleaseBranchName("release/v2.0.0")

        assert branch_1 == branch_2

    def test_equality_components_when_different_value_then_not_equal(self) -> None:
        branch_1 = ReleaseBranchName("release/v1.0.0")
        branch_2 = ReleaseBranchName("release/v2.0.0")

        assert branch_1 != branch_2
