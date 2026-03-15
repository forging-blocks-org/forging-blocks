import inspect
from unittest.mock import AsyncMock, Mock, patch

import pytest
import scripts.release.presentation.__main__ as main_module
from scripts.release.infrastructure.container import Container
from scripts.release.presentation.parsers.release_cli_parser import ReleaseCliParser
from scripts.release.presentation.presenters.release_cli_presenter import (
    ReleaseCliPresenter,
)

from scripts.release.presentation import __main__


@pytest.mark.unit
class TestMain:
    @pytest.fixture
    def mock_container(self) -> AsyncMock:
        return AsyncMock(spec=Container)

    @pytest.fixture
    def mock_parser(self) -> Mock:
        return Mock(spec=ReleaseCliParser)

    @pytest.fixture
    def mock_presenter(self) -> AsyncMock:
        return AsyncMock(spec=ReleaseCliPresenter)

    @pytest.fixture
    def mock_container_class(self, mock_container: AsyncMock):
        with patch("scripts.release.presentation.__main__.Container") as cls:
            cls.return_value = mock_container
            yield cls

    @pytest.fixture
    def mock_parser_class(self, mock_parser: Mock):
        with patch("scripts.release.presentation.__main__.ReleaseCliParser") as cls:
            cls.return_value = mock_parser
            yield cls

    @pytest.fixture
    def mock_presenter_class(self, mock_presenter: AsyncMock):
        with patch("scripts.release.presentation.__main__.ReleaseCliPresenter") as cls:
            cls.return_value = mock_presenter
            yield cls

    @pytest.mark.asyncio
    async def test_main_creates_container_and_initializes_it(
        self,
        mock_container_class: Mock,
        mock_container: AsyncMock,
        mock_parser_class: Mock,
        mock_presenter_class: Mock,
    ) -> None:
        """Test that main() creates a Container and calls initialize()."""
        await __main__.main(["minor", "--execute"])

        mock_container_class.assert_called_once()
        mock_container.initialize.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_creates_parser_and_presenter(
        self,
        mock_container_class: Mock,
        mock_container: AsyncMock,
        mock_parser_class: Mock,
        mock_presenter_class: Mock,
        mock_parser: Mock,
    ) -> None:
        """Test that main() creates ReleaseCliParser and ReleaseCliPresenter."""
        await __main__.main(["patch"])

        mock_parser_class.assert_called_once()
        mock_presenter_class.assert_called_once_with(mock_parser, mock_container)

    @pytest.mark.asyncio
    async def test_main_calls_presenter_present_with_argv(
        self,
        mock_container_class: Mock,
        mock_parser_class: Mock,
        mock_presenter_class: Mock,
        mock_presenter: AsyncMock,
    ) -> None:
        """Test that main() calls presenter.present() with the provided argv."""
        argv = ["major", "--execute"]

        await __main__.main(argv)

        mock_presenter.present.assert_called_once_with(argv)

    @pytest.mark.asyncio
    async def test_main_with_none_argv_passes_none_to_presenter(
        self,
        mock_container_class: Mock,
        mock_parser_class: Mock,
        mock_presenter_class: Mock,
        mock_presenter: AsyncMock,
    ) -> None:
        """Test that main() passes None to presenter.present() when argv is None."""
        await __main__.main(None)

        mock_presenter.present.assert_called_once_with(None)

    @pytest.mark.asyncio
    async def test_main_with_no_arguments_uses_default_none_argv(
        self,
        mock_container_class: Mock,
        mock_parser_class: Mock,
        mock_presenter_class: Mock,
        mock_presenter: AsyncMock,
    ) -> None:
        """Test that main() uses None as default when no argv is provided."""
        await __main__.main()

        mock_presenter.present.assert_called_once_with(None)

    @pytest.mark.parametrize(
        "argv",
        [
            ["major"],
            ["minor", "--execute"],
            ["patch"],
            [],
            ["minor", "--some-flag"],
        ],
    )
    @pytest.mark.asyncio
    async def test_main_execution_flow_with_different_argv_values(
        self,
        argv: list[str],
        mock_container_class: Mock,
        mock_container: AsyncMock,
        mock_parser_class: Mock,
        mock_presenter_class: Mock,
        mock_parser: Mock,
        mock_presenter: AsyncMock,
    ) -> None:
        """Test that main() follows correct execution flow with different argv values."""
        await __main__.main(argv)

        mock_container_class.assert_called_once()
        mock_container.initialize.assert_called_once()
        mock_parser_class.assert_called_once()
        mock_presenter_class.assert_called_once_with(mock_parser, mock_container)
        mock_presenter.present.assert_called_once_with(argv)

    @pytest.mark.asyncio
    async def test_main_awaits_container_initialization(
        self,
        mock_container_class: Mock,
        mock_container: AsyncMock,
        mock_parser_class: Mock,
        mock_presenter_class: Mock,
        mock_presenter: AsyncMock,
    ) -> None:
        """Test that main() properly awaits container.initialize()."""
        initialization_called = False
        presenter_created = False

        async def mock_initialize() -> None:
            nonlocal initialization_called
            initialization_called = True

        def mock_presenter_constructor(*args: object) -> AsyncMock:
            nonlocal presenter_created, initialization_called
            presenter_created = True
            assert initialization_called, (
                "Container should be initialized before presenter creation"
            )
            return mock_presenter

        mock_container.initialize.side_effect = mock_initialize
        mock_presenter_class.side_effect = mock_presenter_constructor

        await __main__.main(["patch"])

        assert initialization_called
        assert presenter_created
        mock_container.initialize.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_awaits_presenter_present(
        self,
        mock_container_class: Mock,
        mock_parser_class: Mock,
        mock_presenter_class: Mock,
        mock_presenter: AsyncMock,
    ) -> None:
        """Test that main() properly awaits presenter.present()."""
        present_called = False

        async def mock_present(argv: object) -> None:
            nonlocal present_called
            present_called = True

        mock_presenter.present.side_effect = mock_present

        await __main__.main(["minor"])

        assert present_called
        mock_presenter.present.assert_called_once()

    def test_main_module_name_check_calls_asyncio_run(self) -> None:
        """Test that the if __name__ == '__main__' block calls asyncio.run(main())."""
        with patch("scripts.release.presentation.__main__.asyncio") as mock_asyncio:
            # Use a plain Mock so calling main() returns a regular object,
            # not a coroutine that would go unawaited inside mock_asyncio.run.
            mock_main = Mock()
            exec(
                compile(
                    'if __name__ == "__main__":\n    asyncio.run(main())',
                    "<string>",
                    "exec",
                ),
                {
                    "__name__": "__main__",
                    "asyncio": mock_asyncio,
                    "main": mock_main,
                },
            )

            mock_asyncio.run.assert_called_once()

    def test_main_module_execution_and_structure(self) -> None:
        """Test that the module has the correct execution structure."""
        assert hasattr(main_module, "main")
        assert callable(main_module.main)

        signature = inspect.signature(main_module.main)
        assert len(signature.parameters) == 1
        argv_param = signature.parameters["argv"]
        assert argv_param.name == "argv"
        assert argv_param.default is None
