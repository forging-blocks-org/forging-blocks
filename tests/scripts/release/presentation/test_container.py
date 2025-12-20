from scripts.release.presentation.container import Container
from scripts.release.application.services.prepare_release_service import (
    PrepareReleaseService,
)
from scripts.release.application.services.create_release_pull_request_service import (
    CreateReleasePullRequestService,
)


class TestContainer:
    def test_prepare_release_use_case_factory(self) -> None:
        container = Container()
        use_case = container.prepare_release_use_case()

        assert isinstance(use_case, PrepareReleaseService)

    def test_create_release_pull_request_use_case_factory(self) -> None:
        container = Container()
        use_case = container.create_release_pull_request_use_case()

        assert isinstance(use_case, CreateReleasePullRequestService)
