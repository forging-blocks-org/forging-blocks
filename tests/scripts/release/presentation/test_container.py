from scripts.release.presentation.container import Container
from scripts.release.application.services.prepare_release_service import (
    PrepareReleaseService,
)
from scripts.release.application.services.open_release_pull_request_service import (
    OpenReleasePullRequestService,
)


class TestContainer:
    def test_prepare_release_use_case_factory(self) -> None:
        container = Container()
        use_case = container.get_prepare_release_use_case()

        assert isinstance(use_case, PrepareReleaseService)

    def test_open_release_pull_request_use_case_factory(self) -> None:
        container = Container()
        use_case = container.get_open_release_pull_request_use_case()

        assert isinstance(use_case, OpenReleasePullRequestService)
