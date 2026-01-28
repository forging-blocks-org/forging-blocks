import pytest
from scripts.release.infrastructure.commons.process import SubprocessCommandRunner


@pytest.mark.integration
class TestSubprocessCommandRunner:
    def test_run_when_command_succeeds_returns_output(self):
        runner = SubprocessCommandRunner()

        result = runner.run(["echo", "Hello, world!"])

        assert result.strip() == "Hello, world!"

    def test_run_when_command_fails_raises_runtime_error(self):
        runner = SubprocessCommandRunner()

        try:
            runner.run(["false"])
        except RuntimeError as e:
            assert "Command failed: false" in str(e)
        else:
            assert False, "Expected RuntimeError was not raised"

    def test_run_with_check_false_returns_output_even_on_failure(self):
        runner = SubprocessCommandRunner()

        result = runner.run(["false"], check=False)

        assert result == ""  # 'false' produces no output

    def test_run_with_suppress_error_log_still_raises_runtime_error(self):
        runner = SubprocessCommandRunner()

        try:
            runner.run(["false"], suppress_error_log=True)
        except RuntimeError as e:
            assert "Command failed: false" in str(e)
        else:
            assert False, "Expected RuntimeError was not raised"
