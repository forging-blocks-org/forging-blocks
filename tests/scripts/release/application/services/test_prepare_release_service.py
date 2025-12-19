import pytest
from unittest.mock import Mock

from scripts.release.application.services.prepare_release_service import (
    PrepareReleaseService,
)
from scripts.release.application.ports.inbound import (
    PrepareReleaseInput,
)
from scripts.release.application.errors import TagAlreadyExistsError
from scripts.release.domain.value_objects import (
    ReleaseLevel,
    ReleaseVersion,
    ReleaseBranchName,
    TagName,
)


class TestPrepareReleaseService:
    async def test_execute_when_tag_already_exists_then_raise_error(self) -> None:
        versioning = Mock()
        vcs = Mock()

        level = ReleaseLevel.from_str("minor")
        version = ReleaseVersion(1, 2, 0)
        tag = TagName.for_version(version)

        versioning.compute_next_version.return_value = version
        vcs.tag_exists.return_value = True

        service = PrepareReleaseService(
            versioning=versioning,
            vcs=vcs,
        )

        request = PrepareReleaseInput(
            level="minor",
            dry_run=False,
        )

        with pytest.raises(TagAlreadyExistsError):
            await service.execute(request)

    async def test_execute_when_branch_exists_and_not_dry_run_then_checkout_and_push(
        self,
    ) -> None:
        versioning = Mock()
        vcs = Mock()

        version = ReleaseVersion(1, 2, 0)
        branch = ReleaseBranchName.from_version(version)

        versioning.compute_next_version.return_value = version
        vcs.tag_exists.return_value = False
        vcs.branch_exists.return_value = True

        service = PrepareReleaseService(
            versioning=versioning,
            vcs=vcs,
        )

        request = PrepareReleaseInput(
            level="minor",
            dry_run=False,
        )

        result = await service.execute(request)

        vcs.checkout.assert_called_once_with(branch)
        vcs.push.assert_called_once_with(
            branch,
            push_tags=False,
        )

        versioning.apply_version.assert_not_called()
        vcs.commit_release_artifacts.assert_not_called()

        assert result.version == "1.2.0"
        assert result.branch == "release/v1.2.0"
        assert result.tag == "v1.2.0"

    async def test_execute_when_branch_does_not_exist_then_create_and_apply_version(
        self,
    ) -> None:
        versioning = Mock()
        vcs = Mock()

        version = ReleaseVersion(1, 2, 0)
        branch = ReleaseBranchName.from_version(version)

        versioning.compute_next_version.return_value = version
        vcs.tag_exists.return_value = False
        vcs.branch_exists.return_value = False

        service = PrepareReleaseService(
            versioning=versioning,
            vcs=vcs,
        )

        request = PrepareReleaseInput(
            level="minor",
            dry_run=False,
        )

        await service.execute(request)

        vcs.create_branch.assert_called_once_with(branch)
        versioning.apply_version.assert_called_once_with(version)
        vcs.commit_release_artifacts.assert_called_once()
        vcs.push.assert_called_once_with(
            branch,
            push_tags=False,
        )

    async def test_execute_when_dry_run_then_no_side_effects(self) -> None:
        versioning = Mock()
        vcs = Mock()

        version = ReleaseVersion(1, 2, 0)

        versioning.compute_next_version.return_value = version
        vcs.tag_exists.return_value = False

        service = PrepareReleaseService(
            versioning=versioning,
            vcs=vcs,
        )

        request = PrepareReleaseInput(
            level="minor",
            dry_run=True,
        )

        result = await service.execute(request)

        vcs.branch_exists.assert_not_called()
        vcs.create_branch.assert_not_called()
        vcs.checkout.assert_not_called()
        vcs.commit_release_artifacts.assert_not_called()
        vcs.push.assert_not_called()
        versioning.apply_version.assert_not_called()

        assert result.version == "1.2.0"
        assert result.branch == "release/v1.2.0"
        assert result.tag == "v1.2.0"
