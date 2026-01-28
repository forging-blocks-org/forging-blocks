from argparse import ArgumentParser, Namespace

import pytest
from scripts.release.presentation.parsers.release_cli_parser import ReleaseCliParser


@pytest.mark.integration
class TestReleaseCliParser:
    @pytest.fixture
    def cli_parser(self) -> ReleaseCliParser:
        return ReleaseCliParser()

    @pytest.mark.parametrize(
        "args, expected_namespace",
        [
            (["major", "--execute"], Namespace(level="major", execute=True)),
            (["minor"], Namespace(level="minor", execute=False)),
            (["patch"], Namespace(level="patch", execute=False)),
        ],
    )
    def test_parse_valid_input(self, cli_parser: ReleaseCliParser, args: list[str], expected_namespace: Namespace) -> None:
        namespace = cli_parser.parse(args)

        assert expected_namespace == namespace

    @pytest.mark.parametrize(
        "args",
        [
            ["wrong", "--execute"],
            ["patch", "--unknown-flag"],
            ["minor", ""],
        ],
    )
    def test_parse_invalid_input_raises_system_exit(self, cli_parser: ReleaseCliParser, args) -> None:
        with pytest.raises(SystemExit) as exc_info:
            cli_parser.parse(args)

        expected_code = 2
        assert expected_code == exc_info.value.code

    def test_init_when_called_then_create_internal_parser(self, cli_parser: ReleaseCliParser) -> None:
        assert cli_parser._argument_parser is not None
        assert cli_parser._argument_parser.prog == "release"
        assert cli_parser._argument_parser.description == "Release automation CLI (presentation layer)."

    def test_parse_with_no_arguments_uses_default_patch_level(self, cli_parser: ReleaseCliParser) -> None:
        """Test that when no level is provided, 'patch' is used as default."""
        namespace = cli_parser.parse([])

        assert namespace.level == "patch"
        assert namespace.execute is False

    def test_parse_with_only_execute_flag_uses_default_patch_level(self, cli_parser: ReleaseCliParser) -> None:
        """Test that when only --execute is provided, 'patch' is used as default level."""
        namespace = cli_parser.parse(["--execute"])

        assert namespace.level == "patch"
        assert namespace.execute is True

    def test_parse_with_none_argv_uses_sys_argv(self, cli_parser: ReleaseCliParser, monkeypatch) -> None:
        """Test that when argv is None, sys.argv is used."""
        # Mock sys.argv to test default behavior
        mock_argv = ["release", "minor", "--execute"]
        monkeypatch.setattr("sys.argv", mock_argv)

        namespace = cli_parser.parse(None)

        assert namespace.level == "minor"
        assert namespace.execute is True

    @pytest.mark.parametrize(
        "invalid_level",
        [
            "invalid",
            "MAJOR",  # Test case sensitivity
            "Major",
            "MINOR",
            "Minor",
            "PATCH",
            "Patch",
            "pre-release",
            "alpha",
            "beta",
            "rc",
            "",
            "0.1.0",
        ],
    )
    def test_parse_invalid_release_levels_raise_system_exit(self, cli_parser: ReleaseCliParser, invalid_level: str) -> None:
        """Test that invalid release levels raise SystemExit with code 2."""
        with pytest.raises(SystemExit) as exc_info:
            cli_parser.parse([invalid_level])

        assert exc_info.value.code == 2

    @pytest.mark.parametrize(
        "valid_level",
        ["major", "minor", "patch"],
    )
    def test_parse_all_valid_release_levels(self, cli_parser: ReleaseCliParser, valid_level: str) -> None:
        """Test that all valid release levels are accepted."""
        namespace = cli_parser.parse([valid_level])

        assert namespace.level == valid_level
        assert namespace.execute is False

    def test_parse_execute_flag_variations(self, cli_parser: ReleaseCliParser) -> None:
        """Test different ways of specifying the execute flag."""
        # Test with level before flag
        namespace1 = cli_parser.parse(["major", "--execute"])
        assert namespace1.level == "major"
        assert namespace1.execute is True

        # Test with flag before level
        namespace2 = cli_parser.parse(["--execute", "minor"])
        assert namespace2.level == "minor"
        assert namespace2.execute is True

    def test_parse_multiple_invalid_flags_raise_system_exit(self, cli_parser: ReleaseCliParser) -> None:
        """Test that multiple invalid flags raise SystemExit."""
        with pytest.raises(SystemExit) as exc_info:
            cli_parser.parse(["patch", "--invalid1", "--invalid2"])

        assert exc_info.value.code == 2

    def test_parse_extra_positional_arguments_raise_system_exit(self, cli_parser: ReleaseCliParser) -> None:
        """Test that extra positional arguments raise SystemExit."""
        with pytest.raises(SystemExit) as exc_info:
            cli_parser.parse(["patch", "extra", "arguments"])

        assert exc_info.value.code == 2

    def test_argument_parser_configuration(self, cli_parser: ReleaseCliParser) -> None:
        """Test that the argument parser is configured correctly."""
        parser = cli_parser._argument_parser

        # Test program name
        assert parser.prog == "release"

        # Test description
        assert parser.description == "Release automation CLI (presentation layer)."

        # Test that parser is an instance of ArgumentParser
        assert isinstance(parser, ArgumentParser)

    def test_help_flag_raises_system_exit_with_code_zero(self, cli_parser: ReleaseCliParser) -> None:
        """Test that --help flag raises SystemExit with code 0."""
        with pytest.raises(SystemExit) as exc_info:
            cli_parser.parse(["--help"])

        assert exc_info.value.code == 0

    def test_version_argument_not_supported(self, cli_parser: ReleaseCliParser) -> None:
        """Test that --version argument is not supported (should raise SystemExit)."""
        with pytest.raises(SystemExit) as exc_info:
            cli_parser.parse(["--version"])

        assert exc_info.value.code == 2

    def test_parse_empty_string_in_arguments_raises_system_exit(self, cli_parser: ReleaseCliParser) -> None:
        """Test that empty string as argument raises SystemExit."""
        with pytest.raises(SystemExit) as exc_info:
            cli_parser.parse([""])

        assert exc_info.value.code == 2

    def test_constructor_creates_new_parser_instance(self) -> None:
        """Test that each ReleaseCliParser instance has its own ArgumentParser."""
        parser1 = ReleaseCliParser()
        parser2 = ReleaseCliParser()

        assert parser1._argument_parser is not parser2._argument_parser

    def test_parse_preserves_argument_order_independence(self, cli_parser: ReleaseCliParser) -> None:
        """Test that argument order doesn't affect the result."""
        namespace1 = cli_parser.parse(["minor", "--execute"])
        namespace2 = cli_parser.parse(["--execute", "minor"])

        assert namespace1.level == namespace2.level
        assert namespace1.execute == namespace2.execute

    def test_parse_level_argument_is_optional_with_default(self, cli_parser: ReleaseCliParser) -> None:
        """Test that the level argument is optional and defaults to 'patch'."""
        # Test with no arguments
        namespace_empty = cli_parser.parse([])
        assert namespace_empty.level == "patch"

        # Test with only --execute flag
        namespace_execute_only = cli_parser.parse(["--execute"])
        assert namespace_execute_only.level == "patch"
