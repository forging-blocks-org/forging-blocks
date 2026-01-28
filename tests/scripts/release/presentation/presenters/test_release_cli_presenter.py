from argparse import Namespace
from logging import Logger
from unittest.mock import AsyncMock, Mock, patch

import pytest
from scripts.release.application.ports.inbound.prepare_release_use_case import (
    PrepareReleaseInput,
    PrepareReleaseOutput,
    PrepareReleaseUseCase,
)
from scripts.release.presentation.container import Container
from scripts.release.presentation.parsers.release_cli_parser import ReleaseCliParser
from scripts.release.presentation.presenters.release_cli_presenter import ReleaseCliPresenter


@pytest.mark.integration
class TestReleaseCliPresenter:
    @pytest.fixture
    def mock_parser(self) -> Mock:
        parser = Mock(spec=ReleaseCliParser)
        return parser

    @pytest.fixture
    def mock_container(self) -> Mock:
        container = Mock(spec=Container)
        return container

    @pytest.fixture
    def mock_use_case(self) -> AsyncMock:
        use_case = AsyncMock(spec=PrepareReleaseUseCase)
        return use_case

    @pytest.fixture
    def presenter(self, mock_parser: Mock, mock_container: Mock) -> ReleaseCliPresenter:
        return ReleaseCliPresenter(parser=mock_parser, container=mock_container)

    @pytest.fixture
    def mock_logger(self) -> Mock:
        logger = Mock(spec=Logger)
        return logger

    async def test_present_when_cli_doesnt_contains_execute_then_logs(
        self,
        presenter: ReleaseCliPresenter,
        mock_parser: Mock,
        mock_container: Mock,
        mock_use_case: AsyncMock,
    ) -> None:
        """Test that presenter handles non-execute mode (dry run) correctly."""
        # Arrange
        argv = ["minor"]
        mock_parser.parse.return_value = Namespace(level="minor", execute=False)
        mock_container.get_prepare_release_use_case.return_value = mock_use_case

        expected_output = PrepareReleaseOutput(version="1.2.0", branch="release/1.2.0", tag="v1.2.0")
        mock_use_case.execute.return_value = expected_output

        with patch.object(presenter, '_logger') as mock_logger:
            # Act
            await presenter.present(argv)

            # Assert
            mock_parser.parse.assert_called_once_with(argv)
            mock_container.get_prepare_release_use_case.assert_called_once()

            expected_input = PrepareReleaseInput(level="minor", dry_run=True)
            mock_use_case.execute.assert_called_once_with(expected_input)

            # Verify logging calls
            assert mock_logger.info.call_count >= 3
            mock_logger.info.assert_any_call("Parsing CLI arguments")
            mock_logger.info.assert_any_call("Preparing release with level: minor, dry_run: True")
            mock_logger.info.assert_any_call("Release preparation completed")
            mock_logger.info.assert_any_call("Dry run mode - no changes were made")

    async def test_present_when_execute_flag_provided_then_executes_release(
        self,
        presenter: ReleaseCliPresenter,
        mock_parser: Mock,
        mock_container: Mock,
        mock_use_case: AsyncMock,
    ) -> None:
        """Test that presenter handles execute mode correctly."""
        # Arrange
        argv = ["major", "--execute"]
        mock_parser.parse.return_value = Namespace(level="major", execute=True)
        mock_container.get_prepare_release_use_case.return_value = mock_use_case

        expected_output = PrepareReleaseOutput(version="2.0.0", branch="release/2.0.0", tag="v2.0.0")
        mock_use_case.execute.return_value = expected_output

        with patch.object(presenter, '_logger') as mock_logger:
            # Act
            await presenter.present(argv)

            # Assert
            mock_parser.parse.assert_called_once_with(argv)
            mock_container.get_prepare_release_use_case.assert_called_once()

            expected_input = PrepareReleaseInput(level="major", dry_run=False)
            mock_use_case.execute.assert_called_once_with(expected_input)

            # Verify logging calls
            assert mock_logger.info.call_count >= 3
            mock_logger.info.assert_any_call("Parsing CLI arguments")
            mock_logger.info.assert_any_call("Preparing release with level: major, dry_run: False")
            mock_logger.info.assert_any_call("Release preparation completed")
            mock_logger.info.assert_any_call("Release executed successfully")

    async def test_present_with_patch_level_dry_run(
        self,
        presenter: ReleaseCliPresenter,
        mock_parser: Mock,
        mock_container: Mock,
        mock_use_case: AsyncMock,
    ) -> None:
        """Test that presenter handles patch level dry run correctly."""
        # Arrange
        argv = ["patch"]
        mock_parser.parse.return_value = Namespace(level="patch", execute=False)
        mock_container.get_prepare_release_use_case.return_value = mock_use_case

        expected_output = PrepareReleaseOutput(version="1.0.1", branch="release/1.0.1", tag="v1.0.1")
        mock_use_case.execute.return_value = expected_output

        with patch.object(presenter, '_logger') as mock_logger:
            # Act
            await presenter.present(argv)

            # Assert
            expected_input = PrepareReleaseInput(level="patch", dry_run=True)
            mock_use_case.execute.assert_called_once_with(expected_input)

            # Verify dry run logging
            mock_logger.info.assert_any_call("Preparing release with level: patch, dry_run: True")
            mock_logger.info.assert_any_call("Dry run mode - no changes were made")

    async def test_present_with_none_argv_passes_none_to_parser(
        self,
        presenter: ReleaseCliPresenter,
        mock_parser: Mock,
        mock_container: Mock,
        mock_use_case: AsyncMock,
    ) -> None:
        """Test that presenter passes None argv to parser correctly."""
        # Arrange
        mock_parser.parse.return_value = Namespace(level="patch", execute=False)
        mock_container.get_prepare_release_use_case.return_value = mock_use_case

        expected_output = PrepareReleaseOutput(version="1.0.1", branch="release/1.0.1", tag="v1.0.1")
        mock_use_case.execute.return_value = expected_output

        # Act
        await presenter.present(None)

        # Assert
        mock_parser.parse.assert_called_once_with(None)

    async def test_present_logs_service_input_and_output_in_debug_mode(
        self,
        presenter: ReleaseCliPresenter,
        mock_parser: Mock,
        mock_container: Mock,
        mock_use_case: AsyncMock,
    ) -> None:
        """Test that presenter logs service input and output in debug mode."""
        # Arrange
        argv = ["minor", "--execute"]
        mock_parser.parse.return_value = Namespace(level="minor", execute=True)
        mock_container.get_prepare_release_use_case.return_value = mock_use_case

        expected_output = PrepareReleaseOutput(version="1.2.0", branch="release/1.2.0", tag="v1.2.0")
        mock_use_case.execute.return_value = expected_output

        with patch.object(presenter, '_logger') as mock_logger:
            # Act
            await presenter.present(argv)

            # Assert
            expected_input = PrepareReleaseInput(level="minor", dry_run=False)

            # Verify debug logging calls
            mock_logger.debug.assert_any_call(f"Service input: {expected_input}")
            mock_logger.debug.assert_any_call(f"Service output: {expected_output}")

    @pytest.mark.parametrize(
        "level, execute, expected_input",
        [
            ("major", True, PrepareReleaseInput(level="major", dry_run=False)),
            ("minor", False, PrepareReleaseInput(level="minor", dry_run=True)),
            ("patch", True, PrepareReleaseInput(level="patch", dry_run=False)),
        ],
    )
    async def test_present_creates_correct_service_input_for_all_levels(
        self,
        presenter: ReleaseCliPresenter,
        mock_parser: Mock,
        mock_container: Mock,
        mock_use_case: AsyncMock,
        level: str,
        execute: bool,
        expected_input: PrepareReleaseInput,
    ) -> None:
        """Test that presenter creates correct service input for all release levels."""
        # Arrange
        mock_parser.parse.return_value = Namespace(level=level, execute=execute)
        mock_container.get_prepare_release_use_case.return_value = mock_use_case

        expected_output = PrepareReleaseOutput(version="1.0.0", branch="release/1.0.0", tag="v1.0.0")
        mock_use_case.execute.return_value = expected_output

        # Act
        await presenter.present([level] + (["--execute"] if execute else []))

        # Assert
        mock_use_case.execute.assert_called_once_with(expected_input)

    async def test_present_handles_use_case_execution_correctly(
        self,
        presenter: ReleaseCliPresenter,
        mock_parser: Mock,
        mock_container: Mock,
        mock_use_case: AsyncMock,
    ) -> None:
        """Test that presenter handles use case execution flow correctly."""
        # Arrange
        argv = ["patch"]
        mock_parser.parse.return_value = Namespace(level="patch", execute=False)
        mock_container.get_prepare_release_use_case.return_value = mock_use_case

        expected_output = PrepareReleaseOutput(version="1.0.1", branch="release/1.0.1", tag="v1.0.1")
        mock_use_case.execute.return_value = expected_output

        with patch.object(presenter, '_logger') as mock_logger:
            # Act
            await presenter.present(argv)

            # Assert execution flow
            # 1. Parse arguments
            mock_parser.parse.assert_called_once_with(argv)

            # 2. Get use case from container
            mock_container.get_prepare_release_use_case.assert_called_once()

            # 3. Execute use case with correct input
            expected_input = PrepareReleaseInput(level="patch", dry_run=True)
            mock_use_case.execute.assert_called_once_with(expected_input)

            # 4. Log completion
            mock_logger.info.assert_any_call("Release preparation completed")

    async def test_constructor_initializes_logger_with_correct_name(
        self,
        mock_parser: Mock,
        mock_container: Mock
    ) -> None:
        """Test that constructor initializes logger with correct name."""
        with patch('scripts.release.presentation.presenters.release_cli_presenter.Logger') as mock_logger_class:
            # Act
            presenter = ReleaseCliPresenter(parser=mock_parser, container=mock_container)

            # Assert
            mock_logger_class.assert_called_once_with('scripts.release.presentation.presenters.release_cli_presenter')
            assert presenter._parser is mock_parser
            assert presenter._container is mock_container

    @pytest.mark.parametrize(
        "execute_flag, expected_dry_run",
        [
            (True, False),   # execute=True -> dry_run=False
            (False, True),   # execute=False -> dry_run=True
        ],
    )
    async def test_present_dry_run_logic_inversion(
        self,
        presenter: ReleaseCliPresenter,
        mock_parser: Mock,
        mock_container: Mock,
        mock_use_case: AsyncMock,
        execute_flag: bool,
        expected_dry_run: bool,
    ) -> None:
        """Test that dry_run is correctly inverted from execute flag."""
        # Arrange
        mock_parser.parse.return_value = Namespace(level="patch", execute=execute_flag)
        mock_container.get_prepare_release_use_case.return_value = mock_use_case

        expected_output = PrepareReleaseOutput(version="1.0.0", branch="release/1.0.0", tag="v1.0.0")
        mock_use_case.execute.return_value = expected_output

        # Act
        await presenter.present(["patch"])

        # Assert
        expected_input = PrepareReleaseInput(level="patch", dry_run=expected_dry_run)
        mock_use_case.execute.assert_called_once_with(expected_input)

    async def test_present_different_log_messages_for_dry_run_vs_execute(
        self,
        presenter: ReleaseCliPresenter,
        mock_parser: Mock,
        mock_container: Mock,
        mock_use_case: AsyncMock,
    ) -> None:
        """Test that different log messages are shown for dry run vs execute modes."""
        expected_output = PrepareReleaseOutput(version="1.0.0", branch="release/1.0.0", tag="v1.0.0")
        mock_use_case.execute.return_value = expected_output
        mock_container.get_prepare_release_use_case.return_value = mock_use_case

        # Test dry run mode
        mock_parser.parse.return_value = Namespace(level="patch", execute=False)

        with patch.object(presenter, '_logger') as mock_logger:
            await presenter.present(["patch"])

            mock_logger.info.assert_any_call("Dry run mode - no changes were made")

            # Verify "Release executed successfully" is NOT called in dry run
            assert not any(
                call for call in mock_logger.info.call_args_list
                if "Release executed successfully" in str(call)
            )

        # Reset mocks
        mock_parser.reset_mock()
        mock_use_case.reset_mock()

        # Test execute mode
        mock_parser.parse.return_value = Namespace(level="patch", execute=True)

        with patch.object(presenter, '_logger') as mock_logger:
            await presenter.present(["patch", "--execute"])

            mock_logger.info.assert_any_call("Release executed successfully")

            # Verify "Dry run mode" message is NOT called in execute mode
            assert not any(
                call for call in mock_logger.info.call_args_list
                if "Dry run mode - no changes were made" in str(call)
            )

    @pytest.mark.parametrize(
        "level, execute, expected_level, expected_dry_run",
        [
            ("major", False, "major", "True"),
            ("minor", True, "minor", "False"),
            ("patch", False, "patch", "True"),
        ],
    )
    async def test_present_logs_preparation_with_correct_parameters(
        self,
        presenter: ReleaseCliPresenter,
        mock_parser: Mock,
        mock_container: Mock,
        mock_use_case: AsyncMock,
        level: str,
        execute: bool,
        expected_level: str,
        expected_dry_run: str,
    ) -> None:
        """Test that preparation logging includes correct level and dry_run parameters."""
        # Arrange
        mock_parser.parse.return_value = Namespace(level=level, execute=execute)
        mock_container.get_prepare_release_use_case.return_value = mock_use_case

        expected_output = PrepareReleaseOutput(version="1.0.0", branch="release/1.0.0", tag="v1.0.0")
        mock_use_case.execute.return_value = expected_output

        with patch.object(presenter, '_logger') as mock_logger:
            # Act
            await presenter.present([level])

            # Assert
            expected_message = f"Preparing release with level: {expected_level}, dry_run: {expected_dry_run}"
            mock_logger.info.assert_any_call(expected_message)
