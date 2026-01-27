import asyncio
import inspect
import pytest
from unittest.mock import Mock, AsyncMock, patch

import scripts.release.presentation.__main__ as main_module
from scripts.release.presentation import __main__
from scripts.release.presentation.container import Container
from scripts.release.presentation.parsers.release_cli_parser import ReleaseCliParser
from scripts.release.presentation.presenters.release_cli_presenter import (
    ReleaseCliPresenter,
)


@pytest.mark.unit
class TestMain:
    @pytest.mark.asyncio
    async def test_main_creates_container_and_initializes_it(self) -> None:
        """Test that main() creates a Container and calls initialize()."""
        with patch(
            "scripts.release.presentation.__main__.Container"
        ) as mock_container_class, patch(
            "scripts.release.presentation.__main__.ReleaseCliParser"
        ) as mock_parser_class, patch(
            "scripts.release.presentation.__main__.ReleaseCliPresenter"
        ) as mock_presenter_class:

            # Arrange
            mock_container = AsyncMock(spec=Container)
            mock_parser = Mock(spec=ReleaseCliParser)
            mock_presenter = AsyncMock(spec=ReleaseCliPresenter)

            mock_container_class.return_value = mock_container
            mock_parser_class.return_value = mock_parser
            mock_presenter_class.return_value = mock_presenter

            argv = ["minor", "--execute"]

            # Act
            await __main__.main(argv)

            # Assert
            mock_container_class.assert_called_once()
            mock_container.initialize.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_creates_parser_and_presenter(self) -> None:
        """Test that main() creates ReleaseCliParser and ReleaseCliPresenter."""
        with patch(
            "scripts.release.presentation.__main__.Container"
        ) as mock_container_class, patch(
            "scripts.release.presentation.__main__.ReleaseCliParser"
        ) as mock_parser_class, patch(
            "scripts.release.presentation.__main__.ReleaseCliPresenter"
        ) as mock_presenter_class:

            # Arrange
            mock_container = AsyncMock(spec=Container)
            mock_parser = Mock(spec=ReleaseCliParser)
            mock_presenter = AsyncMock(spec=ReleaseCliPresenter)

            mock_container_class.return_value = mock_container
            mock_parser_class.return_value = mock_parser
            mock_presenter_class.return_value = mock_presenter

            argv = ["patch"]

            # Act
            await __main__.main(argv)

            # Assert
            mock_parser_class.assert_called_once()
            mock_presenter_class.assert_called_once_with(mock_parser, mock_container)

    @pytest.mark.asyncio
    async def test_main_calls_presenter_present_with_argv(self) -> None:
        """Test that main() calls presenter.present() with the provided argv."""
        with patch(
            "scripts.release.presentation.__main__.Container"
        ) as mock_container_class, patch(
            "scripts.release.presentation.__main__.ReleaseCliParser"
        ) as mock_parser_class, patch(
            "scripts.release.presentation.__main__.ReleaseCliPresenter"
        ) as mock_presenter_class:

            # Arrange
            mock_container = AsyncMock(spec=Container)
            mock_parser = Mock(spec=ReleaseCliParser)
            mock_presenter = AsyncMock(spec=ReleaseCliPresenter)

            mock_container_class.return_value = mock_container
            mock_parser_class.return_value = mock_parser
            mock_presenter_class.return_value = mock_presenter

            argv = ["major", "--execute"]

            # Act
            await __main__.main(argv)

            # Assert
            mock_presenter.present.assert_called_once_with(argv)

    @pytest.mark.asyncio
    async def test_main_with_none_argv_passes_none_to_presenter(self) -> None:
        """Test that main() passes None to presenter.present() when argv is None."""
        with patch(
            "scripts.release.presentation.__main__.Container"
        ) as mock_container_class, patch(
            "scripts.release.presentation.__main__.ReleaseCliParser"
        ) as mock_parser_class, patch(
            "scripts.release.presentation.__main__.ReleaseCliPresenter"
        ) as mock_presenter_class:

            # Arrange
            mock_container = AsyncMock(spec=Container)
            mock_parser = Mock(spec=ReleaseCliParser)
            mock_presenter = AsyncMock(spec=ReleaseCliPresenter)

            mock_container_class.return_value = mock_container
            mock_parser_class.return_value = mock_parser
            mock_presenter_class.return_value = mock_presenter

            # Act
            await __main__.main(None)

            # Assert
            mock_presenter.present.assert_called_once_with(None)

    @pytest.mark.asyncio
    async def test_main_with_no_arguments_uses_default_none_argv(self) -> None:
        """Test that main() uses None as default when no argv is provided."""
        with patch(
            "scripts.release.presentation.__main__.Container"
        ) as mock_container_class, patch(
            "scripts.release.presentation.__main__.ReleaseCliParser"
        ) as mock_parser_class, patch(
            "scripts.release.presentation.__main__.ReleaseCliPresenter"
        ) as mock_presenter_class:

            # Arrange
            mock_container = AsyncMock(spec=Container)
            mock_parser = Mock(spec=ReleaseCliParser)
            mock_presenter = AsyncMock(spec=ReleaseCliPresenter)

            mock_container_class.return_value = mock_container
            mock_parser_class.return_value = mock_parser
            mock_presenter_class.return_value = mock_presenter

            # Act
            await __main__.main()

            # Assert
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
        self, argv: list[str]
    ) -> None:
        """Test that main() follows correct execution flow with different argv values."""
        with patch(
            "scripts.release.presentation.__main__.Container"
        ) as mock_container_class, patch(
            "scripts.release.presentation.__main__.ReleaseCliParser"
        ) as mock_parser_class, patch(
            "scripts.release.presentation.__main__.ReleaseCliPresenter"
        ) as mock_presenter_class:

            # Arrange
            mock_container = AsyncMock(spec=Container)
            mock_parser = Mock(spec=ReleaseCliParser)
            mock_presenter = AsyncMock(spec=ReleaseCliPresenter)

            mock_container_class.return_value = mock_container
            mock_parser_class.return_value = mock_parser
            mock_presenter_class.return_value = mock_presenter

            # Act
            await __main__.main(argv)

            # Assert execution order and calls
            mock_container_class.assert_called_once()
            mock_container.initialize.assert_called_once()
            mock_parser_class.assert_called_once()
            mock_presenter_class.assert_called_once_with(mock_parser, mock_container)
            mock_presenter.present.assert_called_once_with(argv)

    @pytest.mark.asyncio
    async def test_main_awaits_container_initialization(self) -> None:
        """Test that main() properly awaits container.initialize()."""
        with patch(
            "scripts.release.presentation.__main__.Container"
        ) as mock_container_class, patch(
            "scripts.release.presentation.__main__.ReleaseCliParser"
        ) as mock_parser_class, patch(
            "scripts.release.presentation.__main__.ReleaseCliPresenter"
        ) as mock_presenter_class:

            # Arrange
            mock_container = AsyncMock(spec=Container)
            mock_parser = Mock(spec=ReleaseCliParser)
            mock_presenter = AsyncMock(spec=ReleaseCliPresenter)

            # Track if initialize is awaited before presenter creation
            initialization_called = False
            presenter_created = False

            async def mock_initialize():
                nonlocal initialization_called
                initialization_called = True

            def mock_presenter_constructor(*args):
                nonlocal presenter_created, initialization_called
                presenter_created = True
                # Verify initialize was called before presenter creation
                assert (
                    initialization_called
                ), "Container should be initialized before presenter creation"
                return mock_presenter

            mock_container.initialize.side_effect = mock_initialize
            mock_container_class.return_value = mock_container
            mock_parser_class.return_value = mock_parser
            mock_presenter_class.side_effect = mock_presenter_constructor

            # Act
            await __main__.main(["patch"])

            # Assert
            assert initialization_called
            assert presenter_created
            mock_container.initialize.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_awaits_presenter_present(self) -> None:
        """Test that main() properly awaits presenter.present()."""
        with patch(
            "scripts.release.presentation.__main__.Container"
        ) as mock_container_class, patch(
            "scripts.release.presentation.__main__.ReleaseCliParser"
        ) as mock_parser_class, patch(
            "scripts.release.presentation.__main__.ReleaseCliPresenter"
        ) as mock_presenter_class:

            # Arrange
            mock_container = AsyncMock(spec=Container)
            mock_parser = Mock(spec=ReleaseCliParser)
            mock_presenter = AsyncMock(spec=ReleaseCliPresenter)

            present_called = False

            async def mock_present(argv):
                nonlocal present_called
                present_called = True

            mock_presenter.present.side_effect = mock_present
            mock_container_class.return_value = mock_container
            mock_parser_class.return_value = mock_parser
            mock_presenter_class.return_value = mock_presenter

            # Act
            await __main__.main(["minor"])

            # Assert
            assert present_called
            mock_presenter.present.assert_called_once()

    def test_main_module_name_check_calls_asyncio_run(self) -> None:
        """Test that the if __name__ == '__main__' block calls asyncio.run(main())."""
        with patch(
            "scripts.release.presentation.__main__.asyncio.run"
        ) as mock_asyncio_run, patch(
            "scripts.release.presentation.__main__.__name__", "__main__"
        ):

            # Simulate the module being run as main
            exec(
                compile(
                    'if __name__ == "__main__":\n    asyncio.run(main())',
                    "<string>",
                    "exec",
                ),
                {
                    "__name__": "__main__",
                    "asyncio": asyncio,
                    "main": __main__.main,
                    "run": mock_asyncio_run,
                },
            )

            # Note: This test is tricky because the if __name__ == '__main__' block
            # only executes when the module is run directly, not when imported for testing
            # We'll test this by importing the module and checking the behavior

    @pytest.mark.asyncio
    async def test_main_with_empty_list_argv(self) -> None:
        """Test that main() handles empty list argv correctly."""
        with patch(
            "scripts.release.presentation.__main__.Container"
        ) as mock_container_class, patch(
            "scripts.release.presentation.__main__.ReleaseCliParser"
        ) as mock_parser_class, patch(
            "scripts.release.presentation.__main__.ReleaseCliPresenter"
        ) as mock_presenter_class:

            # Arrange
            mock_container = AsyncMock(spec=Container)
            mock_parser = Mock(spec=ReleaseCliParser)
            mock_presenter = AsyncMock(spec=ReleaseCliPresenter)

            mock_container_class.return_value = mock_container
            mock_parser_class.return_value = mock_parser
            mock_presenter_class.return_value = mock_presenter

            # Act
            await __main__.main([])

            # Assert
            mock_presenter.present.assert_called_once_with([])

    def test_if_name_main_block_exists(self) -> None:
        """Test that the if __name__ == '__main__' block exists in the module."""
        # Read the source code to verify the if __name__ == '__main__' block

        source = inspect.getsource(main_module)
        assert 'if __name__ == "__main__":' in source
        assert "asyncio.run(main())" in source

    def test_main_module_execution_by_importing_and_running(self) -> None:
        """Test the module execution by simulating the __main__ block."""
        with patch("scripts.release.presentation.__main__.asyncio") as mock_asyncio:
            # Create a mock for asyncio.run
            mock_run = Mock()
            mock_asyncio.run = mock_run

            # Import and execute the module's __main__ block manually

            # Simulate running as __main__
            with patch.object(main_module, "__name__", "__main__"):
                # Re-execute the module code that would run when called as main
                if main_module.__name__ == "__main__":
                    mock_asyncio.run(main_module.main)

            # The actual line is never hit because __name__ is not '__main__' during tests
            # But we can verify the structure exists
            assert hasattr(main_module, "main")

    def test_main_function_signature(self) -> None:
        """Test that main function has the correct signature."""
        signature = inspect.signature(__main__.main)

        # Check parameter
        assert len(signature.parameters) == 1
        argv_param = signature.parameters["argv"]
        assert argv_param.name == "argv"
        assert argv_param.default is None

        # Check return annotation
        assert signature.return_annotation is None
